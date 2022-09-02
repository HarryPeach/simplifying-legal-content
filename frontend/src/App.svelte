<script>
  import ExtractivePoints from "./lib/ExtractivePoints.svelte";
  import LoadingBar from "./lib/LoadingBar.svelte";
  import SocialButtons from "./lib/SocialButtons.svelte";
  import Spoiler from "./lib/Spoiler.svelte";

  let text_input = "";
  let points = [];
  let current_status = "";

  let headers = new Headers();
  headers.append("Content-Type", "application/json");

  let abstractive_resolved;
  let abstractive_promise = Promise.resolve(abstractive_resolved);

  let summary_length = 40;
  let threshold = 0.725;

  const getExtractiveSummary = async (input) => {
    const extractive = await fetch("http://140.238.69.112:8000/extractive/", {
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
    const abstractive = await fetch("http://140.238.69.112:8000/abstractive/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        text: input,
      }),
    });

    return await abstractive.json();
  };

  const getSeverityClassification = async (input) => {
    const severity = await fetch("http://140.238.69.112:8000/severity/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        items: input,
      }),
    });
    return await severity.json();
  };

  const onButtonClick = async () => {
    // @ts-ignore
    document.querySelector(":root").style.overflow = "hidden";

    current_status = "Creating extractive summary";
    const extractive_summary = await getExtractiveSummary(text_input);
    current_status = "Creating abstractive summary";
    abstractive_promise = await getAbstractiveSummary(extractive_summary);
    current_status = "Classifying severity";
    points = await getSeverityClassification(extractive_summary);
    current_status = "";

    // @ts-ignore
    document.querySelector(":root").style.overflow = "auto";
  };
</script>

<main>
  <LoadingBar status={current_status} />
  <div class="title">
    <h1>LegaTeS</h1>
    <p>
      LegaTeS (Legal Text Simplification) is designed to take in Terms of
      Service documents and Privacy Policies in text form and create simplified
      summaries.
    </p>
  </div>

  <div id="grid-container">
    <div id="grid-item">
      <h2>Terms</h2>
      <span class="explanation"
        >Paste the Terms and Conditions in the text box below, modify the
        settings and then click to process the response.</span
      >
      <SocialButtons bind:input={text_input} />
      <textarea
        rows="10"
        cols="30"
        placeholder="Paste the Terms and Conditions here..."
        bind:value={text_input}
      />
      <Spoiler bind:length={summary_length} bind:threshold />
      <button on:click={onButtonClick}>Generate Summary</button>
      <br />
    </div>
    <div id="grid-item">
      <h2>Abstractive Summary</h2>
      <span class="explanation">
        The <strong>Abstractive Summary</strong> is a summary that attempts to simplify
        a text into a human-readable format. This should be much shorter than the
        original Terms and also use simpler language.
      </span>
      {#await abstractive_promise}
        Awaiting response from server...
      {:then data}
        {#if data == undefined}
          No simplification received yet
        {:else}
          <span>
            {data}
          </span>
        {/if}
      {:catch error}
        There was an error accessing the API: {error}
      {/await}
    </div>
    <div id="grid-item">
      <h2>Extractive Summary</h2>
      <span class="explanation">
        The <strong>Extractive Summary</strong> is a summary that is created
        from verbatim points in the original terms. They are also automatically
        ranked by the "severity" and importance of the terms, with red being a
        <strong>blocker</strong>, yellow being a <strong>bad</strong> point,
        grey being <strong>neutral</strong> and green being
        <strong>good</strong>.
      </span>
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
    width: 40%;
    min-width: 320px;
    margin: auto;
    padding: 50px 0;
  }

  .explanation {
    display: block;
    color: rgba(0, 0, 0, 0.6);
    margin: 20px 0;
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
    border-radius: 10px;
    padding: 20px;
    margin: 20px;
    flex: 1;
    box-shadow: 4px 4px 10px 1px rgba(0, 0, 0, 0.1);
  }

  textarea {
    display: block;
    margin: 2em auto;
    border: 1px solid;
    border-radius: 5px;
  }

  button {
    cursor: pointer;
    border: none;
    border-radius: 10px;
    padding: 2em;
    font-size: 1em;
    background: var(--colour-accent);
    color: white;
    font-weight: bold;
  }
</style>
