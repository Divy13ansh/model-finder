const output = document.getElementById("output");
const findBtn = document.getElementById("find-btn");
const queryInput = document.getElementById("query-input");
const iframe = document.getElementById("api-frame");

let viewerApi = null;

function show(data) {
  output.textContent = JSON.stringify(data, null, 2);
}

async function loadViewer(uid) {
  if (!window.Sketchfab) {
    throw new Error("Sketchfab Viewer API failed to load.");
  }

  const client = new Sketchfab(iframe);

  return new Promise((resolve, reject) => {
    client.init(uid, {
      // Hide Sketchfab's built-in UI so the app can own the controls.
      ui_controls: 0,
      ui_infos: 0,
      ui_stop: 0,
      ui_watermark: 0,
      ui_annotations: 0,
      ui_fullscreen: 0,
      success(api) {
        viewerApi = api;
        api.start();
        api.addEventListener("viewerready", () => {
          resolve();
        });
      },
      error() {
        reject(new Error("Sketchfab viewer initialization failed."));
      },
    });
  });
}

findBtn.addEventListener("click", async () => {
  const query = queryInput.value.trim();

  if (!query) {
    output.textContent = "Please enter a model query.";
    return;
  }

  output.textContent = "Searching Sketchfab...";

  const response = await fetch(`/api/find-model?query=${encodeURIComponent(query)}`);
  const data = await response.json();

  show(data);

  if (!data.uid) {
    return;
  }

  iframe.classList.add("is-loading");
  iframe.src = "";

  try {
    await loadViewer(data.uid);
    iframe.classList.remove("is-loading");
  } catch (error) {
    iframe.classList.remove("is-loading");
    show({ error: error.message });
  }
});
