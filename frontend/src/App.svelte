<script>
  import ExtractivePoints from "./lib/ExtractivePoints.svelte";
  import LoadingBar from "./lib/LoadingBar.svelte";

  let text_input = "";
  let points = [];
  let current_status = "";

  let headers = new Headers();
  headers.append("Content-Type", "application/json");

  let abstractive_resolved;
  let abstractive_promise = Promise.resolve(abstractive_resolved);

  const getExtractiveSummary = async (input) => {
    const extractive = await fetch("http://127.0.0.1:8000/extractive/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        text: input,
        threshold: 0.5,
      }),
    });

    return await extractive.json();
  };

  const getAbstractiveSummary = async (input) => {
    const abstractive = await fetch("http://127.0.0.1:8000/abstractive/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        text: input,
      }),
    });

    return await abstractive.json();
  };

  const getSeverityClassification = async (input) => {
    const severity = await fetch("http://127.0.0.1:8000/severity/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        items: input,
      }),
    });
    return await severity.json();
  };

  const onButtonClick = async () => {
    current_status = "Creating extractive summary";
    const extractive_summary = await getExtractiveSummary(text_input);
    current_status = "Creating abstractive summary";
    abstractive_promise = await getAbstractiveSummary(extractive_summary);
    current_status = "Classifying severity";
    points = await getSeverityClassification(extractive_summary);
    current_status = "";
  };
</script>

<main>
  <LoadingBar status={current_status} />
  <div class="title">
    <h1>Terms and Conditions Simplifier</h1>
    <p>
      This service is designed to take in a Terms of Service in text form and
      create simplified summaries for you!
    </p>
  </div>

  <div id="grid-container">
    <div id="grid-item">
      <h2>Terms</h2>
      <textarea
        rows="10"
        cols="30"
        placeholder="Paste the Terms and Conditions here..."
        bind:value={text_input}
      />
      <button on:click={onButtonClick}>Click to receive response</button>
      <br />
    </div>
    <div id="grid-item">
      <h2>Abstractive Summary</h2>
      {#await abstractive_promise}
        Awaiting response from server...
      {:then data}
        {#if data == undefined}
          No simplification received yet
        {:else}
          {data}
        {/if}
      {:catch error}
        There was an error accessing the API: {error}
      {/await}
    </div>
    <div id="grid-item">
      <h2>Extractive Summary</h2>
      <ExtractivePoints {points} />
    </div>
  </div>
  <footer>Created by Harry Peach &copy;</footer>
</main>

<style>
  :root {
    --primary-text-color: rgb(197, 32, 32);
    font-family: sans-serif;
  }

  .title {
    width: 30%;
    min-width: 320px;
    margin: auto;
  }
  main {
    text-align: center;
    margin: 0 auto;
  }

  main textarea {
    width: 100%;
    resize: vertical;
  }

  #grid-container {
    text-align: center;
    display: flex;
    flex-wrap: wrap;
    margin: auto;
    grid-template-columns: auto auto auto;
  }

  #grid-item {
    min-width: 320px;
    border: 1px dotted red;
    padding: 20px;
    margin: 20px;
    flex: 1;
  }

  textarea {
    display: block;
    margin: 2em auto;
    border: 1px solid;
    border-radius: 5px;
  }

  button {
    border: none;
    border-radius: 5px;
    padding: 2em;
    font-size: 1em;
  }
</style>
