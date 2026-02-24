/**
 * Gestor de carga de datos desde archivos CSV
 */
import { CSVParser } from './csvParser.js';

export class DataLoader {
    constructor() {
        this.peliculas = [];
        this.generos = [];
        this.loaded = false;
    }

    /**
     * Carga todos los archivos CSV necesarios
     * @returns {Promise<void>}
     */
    async loadAll() {
        try {
            const [peliculasText, generosText] = await Promise.all([
                this.fetchCSV('./peliculas.csv'),
                this.fetchCSV('./generos.csv')
            ]);

            this.peliculas = CSVParser.parse(peliculasText);
            this.generos = CSVParser.parse(generosText);

            // Procesar películas para añadir información adicional
            this.peliculas = this.peliculas.map(pelicula => ({
                ...pelicula,
                puntuacion: CSVParser.parseScore(pelicula.puntuacion_media),
                votosNum: parseInt(pelicula.votos) || 0,
                posterUrl: pelicula.poster_path
                    ? `https://image.tmdb.org/t/p/w500${pelicula.poster_path}`
                    : 'https://via.placeholder.com/500x750?text=Sin+Imagen'
            }));

            this.loaded = true;
            console.log(`✅ Datos cargados: ${this.peliculas.length} películas, ${this.generos.length} géneros`);
        } catch (error) {
            console.error('❌ Error cargando datos:', error);
            throw error;
        }
    }

    /**
     * Obtiene contenido de un archivo CSV
     * @param {string} url - URL del archivo CSV
     * @returns {Promise<string>} Contenido del archivo
     */
    async fetchCSV(url) {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error cargando ${url}: ${response.statusText}`);
        }
        return await response.text();
    }

    /**
     * Busca películas por título
     * @param {string} query - Término de búsqueda
     * @returns {Array<Object>} Películas que coinciden
     */
    searchByTitle(query) {
        if (!query) return this.peliculas;

        const searchTerm = query.toLowerCase();
        return this.peliculas.filter(pelicula =>
            pelicula.titulo.toLowerCase().includes(searchTerm)
        );
    }

    /**
     * Filtra películas por género
     * @param {string} generoId - ID del género
     * @returns {Array<Object>} Películas del género
     */
    filterByGenero(generoId) {
        if (!generoId || generoId === 'all') return this.peliculas;

        return this.peliculas.filter(pelicula => {
            // Buscar en todas las columnas de género (id_genero, id_genero.1, etc.)
            for (let key in pelicula) {
                if (key.startsWith('id_genero') && pelicula[key] === generoId) {
                    return true;
                }
            }
            return false;
        });
    }

    /**
     * Obtiene lista de géneros únicos
     * @returns {Array<Object>} Lista de géneros
     */
    getGeneros() {
        return this.generos;
    }
}
