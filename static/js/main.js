// const var_re = document.getElementById("re");
// var_re.addEventListener("click", (e) => {
//   fetch("/api").then((res) => console.log(res));
// });

class Paste {
  constructor() {
    this.btn = document.querySelector(".btn");
    this.editor = CodeMirror(document.getElementById("textArea"), {
      placeholder: "Paste code, save and share the link!",
      lineNumbers: true,
      theme: "darcula",
    });
  }

  async request(content) {
    let responce = await fetch("api", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });
    console.log(await responce.json());
  }

  save() {
    this.btn.addEventListener("click", (_) => {
      let content = this.editor.getDoc().getValue();
      if (!content) return;
      this.request(content);
    });
  }
}

window.addEventListener("DOMContentLoaded", async (_) => {
  codeEditor = new CodeMirror();
  const past = new Paste();
  past.save();
});

// var lineCountCache = 0;
// const lineNumber = document.getElementById("lineCounter");
// const userTextarea = document.getElementById("userTextarea");

// const lengthOftextarea = (text) => {
//   return text.length ? text.split(/\r\n|\r|\n/).length : 0;
// };

// const lineCounter = (lineCount) => {
//   var lineCountList = [];
//   if (lineCountCache == lineCount) return;
//   for (var number = 0; number < lineCount; number++) {
//     lineCountList.push(`${number + 1}. `);
//   }
//   lineNumber.textContent = lineCountList.join("\n");
// };
// userTextarea.addEventListener("input", userTextCount);
// function userTextCount(e) {
//   let text = e.target.value;
//   let lineCount = lengthOftextarea(text);

//   lineCounter(lineCount);
// }

// userTextarea.addEventListener("keydown", (e) => {
//   let keyCode = e.keyCode;
//   switch (keyCode) {
//     case 8:
//       let textlength = userTextarea.value.length;
//       console.log(textlength);

//       if (textlength != 0) {
//         lineNumber.textContent = " ";
//       }
//       break;
//     default:
//       return;
//   }
// });
