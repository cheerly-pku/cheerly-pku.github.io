# Jiaqi Li

Undergraduate student at the [College of Engineering](https://www.coe.pku.edu.cn/), [Peking University](https://www.pku.edu.cn/).

I am interested in mathematics, mechanics, computer science, and intelligent science. I also build practice and review websites for courses that I have studied. I participate in undergraduate research with [Assoc. Prof. Mohan Chen](http://www2.coe.pku.edu.cn/subpaget.asp?id=663)'s [research group](http://www2.coe.pku.edu.cn/subpaget.asp?id=664) at Peking University.

[Homepage](https://cheerly-pku.github.io/) | [CV](https://cheerly-pku.github.io/cv/Jiaqi_Li_CV.pdf) | [Email](mailto:jq_li25@stu.pku.edu.cn)

For publications, projects, updates, and links, please visit the [homepage](https://cheerly-pku.github.io/).

## Repository Structure

- `src/pages/`: Astro page sources.
- `src/components/`: shared page components, including GitHub-powered comments.
- `src/layouts/`: shared document layout and client-side behavior.
- `src/styles/`: shared responsive styling.
- `public/images/`: profile, favicon, and friend images.
- `public/cv/`: published English and Chinese CVs.
- `public/linear-algebra-practice/`: standalone linear algebra course website.
- `public/parallel-practice/`: standalone parallel programming course website.
- `scripts/`: local maintenance utilities.
- `.github/workflows/`: automatic GitHub Pages deployment.

## Local Development

```powershell
npm install
npm run dev
npm run build
npm run preview
```

Pushing to `main` runs the Pages workflow. Astro builds the site into the ignored `dist/` directory, and GitHub Actions deploys that artifact automatically. Generated HTML and hashed CSS should not be copied back into the repository root.
