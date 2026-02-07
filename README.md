# Kartoza Website

> **A Happy Life is a Mappy Life**

Official website for [Kartoza](https://kartoza.com) - Open Source Geospatial Experts.

## About Kartoza

Kartoza is a global Free and Open Source GIS (FOSS GIS) service provider registered in South Africa and Portugal. We use GIS software to address location-related challenges for individuals, businesses, and governments worldwide.

### Our Vision

> Enable a world where spatial decision making tools are **universal**, **accessible** and **affordable** for everyone for the benefit of the planet and people.

## Technology Stack

This website is built with:

- **[Hugo](https://gohugo.io/)** - Static site generator
- **[Bulma](https://bulma.io/)** - CSS framework
- **Custom Hugo theme** - hugo-bulma-blocks-theme

## Project Structure

```plaintext
Kartoza-Hugo/
├── content/           # Markdown content files
│   ├── about/         # About page
│   ├── apps/          # Mobile and web applications
│   ├── blog/          # Blog posts
│   ├── careers/       # Job listings
│   ├── gallery/       # Image gallery
│   ├── portfolio/     # Project portfolio
│   ├── solutions/     # Solutions and services
│   ├── the_team/      # Team members
│   └── training-courses/  # Training offerings
├── layouts/           # Custom Hugo templates
├── static/            # Static assets (images, etc.)
└── themes/            # Hugo theme
```

## Development

### Prerequisites

- Hugo (extended version recommended)
- Git

### Using Nix Shell

If you have Nix installed, you can use the provided shell environment:

```bash
nix-shell -p hugo
```

### Running Locally

```bash
# Start the development server
hugo server -D

# Build for production
hugo
```

The site will be available at `http://localhost:1313`

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contact

- **Website:** [kartoza.com](https://kartoza.com)
- **Email:** info@kartoza.com
- **Phone:** +27 21 813 8912

---

Made with love by the Kartoza team.
