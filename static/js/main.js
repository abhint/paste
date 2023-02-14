class Paste {
  constructor() {
    this.btn = document.getElementById("save");
    this.urlText = document.querySelector(".key");
    this.editor = CodeMirror(document.getElementById("textArea"), {
      placeholder: "Paste your note",
      lineNumbers: true,
      theme: "darcula",
    });
  }

  async copy(url) {
    // https://stackoverflow.com/a/45071478/11913751

    this.urlText.onclick = function () {
      document.execCommand("copy");
    };

    this.urlText.addEventListener("copy", function (event) {
      event.preventDefault();
      if (event.clipboardData) {
        event.clipboardData.setData("text/plain", url);
        console.log(event.clipboardData.getData("text"));
      }
    });
  }

  async request(content) {
    let response = await fetch("api", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });
    let result = await response.json()
    console.log(result);
    if (response.ok) return (window.location = `/${result.key}`);
  }

  save() {
    this.btn.addEventListener("click", (_) => {
      let content = this.editor.getDoc().getValue();
      if (!content) return;
      this.request(content);
    });
  }

  async load() {
    let urlPath = window.location.pathname;
    if (urlPath === "/") return;
    let response = await fetch(`/api/p${urlPath}`, {
      method: "POST",
    });

    if (!response.ok) return (window.location = "/");
    this.btn.style.visibility = "hidden";
    let result = await response.json();

    this.editor.getDoc().setValue(result.content);
    this.editor.setOption("readOnly", true);

    this.urlText.innerHTML = `/${result.key}`;
    await this.copy(`${window.location.origin}/${result.key}`);
  }
}

window.addEventListener("DOMContentLoaded", async (_) => {
  codeEditor = new CodeMirror();
  const past = new Paste();
  past.save();
  past.load();
});
