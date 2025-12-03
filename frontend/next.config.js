/** next.config.js */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "your-domain.com",
      },
    ],
  },
}

module.exports = nextConfig
