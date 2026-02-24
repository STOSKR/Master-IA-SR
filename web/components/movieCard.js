/**
 * Componente para renderizar una tarjeta de película
 */
export class MovieCard {
    /**
     * Crea el HTML de una tarjeta de película
     * @param {Object} pelicula - Datos de la película
     * @returns {string} HTML de la tarjeta
     */
    static render(pelicula) {
        const { titulo, posterUrl, puntuacion, votosNum, imdb_id } = pelicula;
        const imdbLink = imdb_id ? `https://www.imdb.com/title/${imdb_id}/` : '#';

        return `
      <div class="movie-card" data-movie-id="${pelicula.id}">
        <div class="movie-poster">
          <img src="${posterUrl}" alt="${titulo}" loading="lazy" onerror="this.src='https://via.placeholder.com/500x750?text=Sin+Imagen'">
          <div class="movie-rating">
            <span class="rating-star">⭐</span>
            <span class="rating-value">${puntuacion.toFixed(1)}</span>
          </div>
        </div>
        <div class="movie-info">
          <h3 class="movie-title">${this.escapeHtml(titulo)}</h3>
          <div class="movie-stats">
            <span class="votes">👥 ${this.formatVotes(votosNum)} votos</span>
          </div>
          ${imdb_id ? `<a href="${imdbLink}" target="_blank" class="imdb-link" rel="noopener">Ver en IMDb →</a>` : ''}
        </div>
      </div>
    `;
    }

    /**
     * Escapa caracteres HTML para prevenir XSS
     * @param {string} text - Texto a escapar
     * @returns {string} Texto escapado
     */
    static escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Formatea el número de votos para mostrar
     * @param {number} votes - Número de votos
     * @returns {string} Número formateado
     */
    static formatVotes(votes) {
        if (votes >= 1000) {
            return (votes / 1000).toFixed(1) + 'k';
        }
        return votes.toString();
    }
}
