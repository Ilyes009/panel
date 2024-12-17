export const API_CONFIG = {
  // Remplacer par l'URL de votre serveur backend Python
  baseURL: import.meta.env.VITE_API_URL || 'https://your-python-backend.herokuapp.com',
  endpoints: {
    auth: '/auth',
    marketplace: '/api/marketplace',
    accounts: '/api/accounts'
  }
};