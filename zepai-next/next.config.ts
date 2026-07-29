import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Exportacion estatica: el sitio se sigue sirviendo como HTML plano.
  // Es lo que conserva la velocidad y el SEO que ya teniamos; Next aporta
  // el sistema de componentes, con lo que nav y pie dejan de estar
  // duplicados en 12 ficheros (era el 41% del HTML).
  output: "export",

  // Sin servidor no hay optimizador de imagenes en tiempo real.
  images: { unoptimized: true },

  // URLs sin barra final: /soluciones, no /soluciones/.
  // Debe coincidir con vercel.json o rompemos los canonical.
  trailingSlash: false,
};

export default nextConfig;
