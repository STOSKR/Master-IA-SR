/**
 * Componente de panel de filtros
 */
export class FilterPanel {
    constructor(generos, onFilter) {
        this.generos = generos;
        this.onFilter = onFilter;
        this.selectedGenero = 'all';
        this.sortBy = 'puntuacion';
    }

    /**
     * Renderiza el HTML del panel de filtros
     * @returns {string} HTML del panel
     */
    render() {
        return `
      <div class="filter-panel">
        <div class="filter-group">
          <label for="generoFilter" class="filter-label">
            <span class="filter-icon">🎬</span>
            Género
          </label>
          <select id="generoFilter" class="filter-select">
            <option value="all">Todos los géneros</option>
            ${this.generos.map(g => `
              <option value="${g.IdDataset}">${g.GeneroSP || g.Genero}</option>
            `).join('')}
          </select>
        </div>

        <div class="filter-group">
          <label for="sortFilter" class="filter-label">
            <span class="filter-icon">📊</span>
            Ordenar por
          </label>
          <select id="sortFilter" class="filter-select">
            <option value="puntuacion">Mejor puntuación</option>
            <option value="votos">Más votadas</option>
            <option value="titulo">Título (A-Z)</option>
          </select>
        </div>
      </div>
    `;
    }

    /**
     * Inicializa los event listeners
     */
    init() {
        const generoFilter = document.getElementById('generoFilter');
        const sortFilter = document.getElementById('sortFilter');

        if (generoFilter) {
            generoFilter.addEventListener('change', (e) => {
                this.selectedGenero = e.target.value;
                this.applyFilters();
            });
        }

        if (sortFilter) {
            sortFilter.addEventListener('change', (e) => {
                this.sortBy = e.target.value;
                this.applyFilters();
            });
        }
    }

    /**
     * Aplica los filtros actuales
     */
    applyFilters() {
        this.onFilter({
            genero: this.selectedGenero,
            sortBy: this.sortBy
        });
    }

    /**
     * Ordena un array de películas según el criterio seleccionado
     * @param {Array} peliculas - Array de películas
     * @returns {Array} Array ordenado
     */
    sortMovies(peliculas) {
        const sorted = [...peliculas];

        switch (this.sortBy) {
            case 'puntuacion':
                return sorted.sort((a, b) => b.puntuacion - a.puntuacion);
            case 'votos':
                return sorted.sort((a, b) => b.votosNum - a.votosNum);
            case 'titulo':
                return sorted.sort((a, b) => a.titulo.localeCompare(b.titulo));
            default:
                return sorted;
        }
    }
}
