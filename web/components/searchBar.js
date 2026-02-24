/**
 * Componente de barra de búsqueda
 */
export class SearchBar {
    constructor(onSearch) {
        this.onSearch = onSearch;
        this.debounceTimer = null;
    }

    /**
     * Renderiza el HTML del componente
     * @returns {string} HTML de la barra de búsqueda
     */
    render() {
        return `
      <div class="search-container">
        <div class="search-wrapper">
          <span class="search-icon">🔍</span>
          <input 
            type="text" 
            id="searchInput" 
            class="search-input" 
            placeholder="Buscar películas por título..."
            autocomplete="off"
          >
          <button id="clearSearch" class="clear-button" style="display: none;">✕</button>
        </div>
      </div>
    `;
    }

    /**
     * Inicializa los event listeners
     */
    init() {
        const searchInput = document.getElementById('searchInput');
        const clearButton = document.getElementById('clearSearch');

        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const value = e.target.value;

                // Mostrar/ocultar botón de limpiar
                clearButton.style.display = value ? 'block' : 'none';

                // Debounce para evitar búsquedas excesivas
                clearTimeout(this.debounceTimer);
                this.debounceTimer = setTimeout(() => {
                    this.onSearch(value);
                }, 300);
            });

            // Enter para buscar inmediatamente
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    clearTimeout(this.debounceTimer);
                    this.onSearch(e.target.value);
                }
            });
        }

        if (clearButton) {
            clearButton.addEventListener('click', () => {
                searchInput.value = '';
                clearButton.style.display = 'none';
                this.onSearch('');
                searchInput.focus();
            });
        }
    }
}
