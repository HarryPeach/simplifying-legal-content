<script>
  let promise = Promise.resolve([]);
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
  <h1>Terms and Conditions Simplifier</h1>

  <textarea
    rows="20"
    cols="60"
    placeholder="Paste the Terms and Conditions here..."
  />

  <button on:click={onButtonClick}>Click to receive response</button>

  <br />

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
</main>

<style>
  :root {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  }

  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
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
