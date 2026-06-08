/**
 * Utility to determine the best contrasting text color (black or white) for a given background color.
 * @param {string} hexcolor - The background color in hex format.
 * @returns {string} - '#000000' for light backgrounds, '#ffffff' for dark backgrounds.
 */
export const getContrastColor = (hexcolor) => {
  if (!hexcolor || typeof hexcolor !== 'string') return '#000000';
  let hex = hexcolor.replace('#', '');
  if (hex.length === 3) hex = hex.split('').map(s => s + s).join('');
  if (hex.length !== 6) return '#000000';
  
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  // YIQ formula
  const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
  return (yiq >= 128) ? '#000000' : '#ffffff';
};

/**
 * Checks if a color is "dark".
 * @param {string} hexcolor 
 * @returns {boolean}
 */
export const isDark = (hexcolor) => {
    return getContrastColor(hexcolor) === '#ffffff';
};

/**
 * Adjusts a color's opacity if it's hex.
 * @param {string} hex 
 * @param {number} opacity 
 * @returns {string}
 */
export const hexToRgba = (hex, opacity = 1) => {
    let h = hex.replace('#', '');
    if (h.length === 3) h = h.split('').map(s => s + s).join('');
    const r = parseInt(h.substr(0, 2), 16);
    const g = parseInt(h.substr(2, 2), 16);
    const b = parseInt(h.substr(4, 2), 16);
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
};
