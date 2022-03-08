<script>
  import ExtractivePoints from "./lib/ExtractivePoints.svelte";

  let resolved = { abstractive: "", extractive: "" };
  let promise = Promise.resolve(resolved);
  const fetchResponse = async () => {
    const response = await fetch("http://127.0.0.1:8000");
    const data = await response.json();
    console.debug(data);
    return data;
  };

  const onButtonClick = () => {
    promise = fetchResponse();
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
      />
      <button on:click={onButtonClick}>Click to receive response</button>
      <br />
    </div>
    <div id="grid-item">
      <h2>Abstractive Summary</h2>
      {#await promise}
        Awaiting response from server...
      {:then data}
        {#if data.abstractive == undefined}
          No simplification received yet
        {:else}
          {data.abstractive}
        {/if}
      {:catch error}
        There was an error accessing the API: {error}
      {/await}
    </div>
    <div id="grid-item">
      <h2>Extractive Summary</h2>
      <ExtractivePoints
        points={[
          { point: "Critical Point", level: "critical" },
          { point: "Another Critical Point", level: "critical" },
          { point: "Warn Point", level: "warn" },
          { point: "Neutral Point", level: "neutral" },
          { point: "Another Neutral Point", level: "neutral" },
          { point: "Another Neutral Point", level: "neutral" },
          { point: "Good Point", level: "good" },
        ]}
      />
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
