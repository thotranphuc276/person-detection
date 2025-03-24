const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost/api',
  env: process.env.NEXT_PUBLIC_ENV || 'development',
  isDev: (process.env.NEXT_PUBLIC_ENV || 'development') === 'development',
  isProd: process.env.NEXT_PUBLIC_ENV === 'production',
};

export default config; 