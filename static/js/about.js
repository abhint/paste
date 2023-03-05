class AboutSection {
  constructor() {
    this.about = document.getElementById("about");
  }
  async getReadme() {
    let response = await fetch(
      "https://api.github.com/repos/abhint/paste/contents/README.md?ref=master"
    );
    let content = await response.text();
    this.about.innerHTML = marked.parse(content);
    console.log();
  }
}

window.addEventListener("DOMContentLoaded", async (_) => {
  let aboutSection = new AboutSection();
  aboutSection.getReadme();
});
