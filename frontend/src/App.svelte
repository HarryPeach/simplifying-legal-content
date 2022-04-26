<script>
  import ExtractivePoints from "./lib/ExtractivePoints.svelte";

  let text_input = "";
  let points = [];

  let headers = new Headers();
  headers.append("Content-Type", "application/json");

  let abstractive_resolved = undefined;
  let abstractive_promise = Promise.resolve(abstractive_resolved);

  const getExtractiveSummary = async (input) => {
    const extractive = await fetch("http://127.0.0.1:8000/extractive/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        text: input,
        threshold: 0.725,
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
    const severity = await fetch("http://127.0.0.1:8000/severity", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        items: input,
      }),
    });
    return await severity.json();
  };

  const onButtonClick = async () => {
    console.debug("Getting extractive summary");
    const extractive_summary = await getExtractiveSummary(text_input);
    console.debug("Getting abstractive summary");
    abstractive_promise = await getAbstractiveSummary(extractive_summary);
    console.debug("Getting severity classification");
    points = await getSeverityClassification(extractive_summary);
  };
</script>

<main>
  <div class="title">
    <h1>Terms and Conditions Simplifier</h1>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam placerat a
      leo eu vestibulum. Vestibulum pulvinar dolor eu diam congue, at interdum
      erat sollicitudin. Aliquam feugiat efficitur lectus sollicitudin varius.
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
    padding: 1em;
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
