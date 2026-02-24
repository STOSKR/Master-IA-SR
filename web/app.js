/**
 * Aplicación principal - Orquesta todos los componentes
 */
import { DataLoader } from './utils/dataLoader.js';
import { MovieCard } from './components/movieCard.js';
import { SearchBar } from './components/searchBar.js';
import { FilterPanel } from './components/filterPanel.js';

class MovieSearchApp {
    constructor() {
        this.dataLoader = new DataLoader();
        this.searchBar = null;
        this.filterPanel = null;
        this.currentResults = [];
        this.currentQuery = '';
    }

    /**
     * Inicializa la aplicación
     */
    async init() {
        try {
            this.showLoading(true);

            // Cargar datos
            await this.dataLoader.loadAll();

            // Inicializar componentes
            this.initializeComponents();

            // Mostrar todas las películas inicialmente
            this.displayMovies(this.dataLoader.peliculas);

            this.showLoading(false);
        } catch (error) {
            console.error('Error inicializando app:', error);
            this.showError('Error cargando los datos. Por favor, recarga la página.');
        }
    }

    /**
     * Inicializa todos los componentes de la UI
     */
    initializeComponents() {
        // Inicializar SearchBar
        this.searchBar = new SearchBar((query) => this.handleSearch(query));
        document.getElementById('searchBarContainer').innerHTML = this.searchBar.render();
        this.searchBar.init();

        // Inicializar FilterPanel
        this.filterPanel = new FilterPanel(
            this.dataLoader.getGeneros(),
            (filters) => this.handleFilter(filters)
        );
        document.getElementById('filterPanelContainer').innerHTML = this.filterPanel.render();
        this.filterPanel.init();
    }

    /**
     * Maneja la búsqueda de películas
     * @param {string} query - Término de búsqueda
     */
    handleSearch(query) {
        this.currentQuery = query;
        this.applyCurrentFilters();
    }

    /**
     * Maneja el filtrado de películas
     * @param {Object} filters - Filtros aplicados
     */
    handleFilter(filters) {
        this.applyCurrentFilters();
    }

    /**
     * Aplica todos los filtros y búsquedas actuales
     */
    applyCurrentFilters() {
        let results = this.dataLoader.peliculas;

        // Aplicar búsqueda por título
        if (this.currentQuery) {
            results = this.dataLoader.searchByTitle(this.currentQuery);
        }

        // Aplicar filtro de género
        if (this.filterPanel.selectedGenero !== 'all') {
            results = results.filter(pelicula => {
                for (let key in pelicula) {
                    if (key.startsWith('id_genero') && pelicula[key] === this.filterPanel.selectedGenero) {
                        return true;
                    }
                }
                return false;
            });
        }

        // Aplicar ordenamiento
        results = this.filterPanel.sortMovies(results);

        this.displayMovies(results);
    }

    /**
     * Muestra las películas en el grid
     * @param {Array} peliculas - Array de películas a mostrar
     */
    displayMovies(peliculas) {
        this.currentResults = peliculas;
        const container = document.getElementById('moviesGrid');
        const resultsCount = document.getElementById('resultsCount');

        if (!container) return;

        // Actualizar contador de resultados
        if (resultsCount) {
            resultsCount.textContent = `${peliculas.length} película${peliculas.length !== 1 ? 's' : ''} encontrada${peliculas.length !== 1 ? 's' : ''}`;
        }

        // Mostrar mensaje si no hay resultados
        if (peliculas.length === 0) {
            container.innerHTML = `
        <div class="no-results">
          <div class="no-results-icon">🎬</div>
          <h3>No se encontraron películas</h3>
          <p>Intenta con otros términos de búsqueda o filtros</p>
        </div>
      `;
            return;
        }

        // Renderizar películas
        container.innerHTML = peliculas
            .map(pelicula => MovieCard.render(pelicula))
            .join('');
    }

    /**
     * Muestra/oculta el indicador de carga
     * @param {boolean} show - Si mostrar o no el loading
     */
    showLoading(show) {
        const loader = document.getElementById('loader');
        const content = document.getElementById('mainContent');

        if (loader) loader.style.display = show ? 'flex' : 'none';
        if (content) content.style.display = show ? 'none' : 'block';
    }

    /**
     * Muestra un mensaje de error
     * @param {string} message - Mensaje a mostrar
     */
    showError(message) {
        const container = document.getElementById('moviesGrid');
        if (container) {
            container.innerHTML = `
        <div class="error-message">
          <div class="error-icon">⚠️</div>
          <h3>Error</h3>
          <p>${message}</p>
        </div>
      `;
        }
        this.showLoading(false);
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const app = new MovieSearchApp();
    app.init();
});
