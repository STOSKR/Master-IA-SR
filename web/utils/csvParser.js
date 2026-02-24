/**
 * Utilidad para parsear archivos CSV con delimitador de punto y coma
 */
export class CSVParser {
    /**
     * Parsea un archivo CSV y retorna un array de objetos
     * @param {string} csvText - Contenido del archivo CSV
     * @param {string} delimiter - Delimitador usado (por defecto ';')
     * @returns {Array<Object>} Array de objetos donde cada objeto representa una fila
     */
    static parse(csvText, delimiter = ';') {
        const lines = csvText.trim().split('\n');
        if (lines.length === 0) return [];

        // Obtener headers
        const headers = lines[0].split(delimiter).map(h => h.trim());

        // Parsear filas
        const data = [];
        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(delimiter);

            if (values.length === headers.length) {
                const row = {};
                headers.forEach((header, index) => {
                    row[header] = values[index]?.trim() || '';
                });
                data.push(row);
            }
        }

        return data;
    }

    /**
     * Convierte puntuación de formato español (6,5) a número
     * @param {string} score - Puntuación en formato string
     * @returns {number} Puntuación como número
     */
    static parseScore(score) {
        if (!score) return 0;
        return parseFloat(score.replace(',', '.'));
    }
}
