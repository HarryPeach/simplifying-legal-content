<script>
  import { Jumper } from "svelte-loading-spinners";
  export let status;
</script>

<main class={status == "" ? "hidden" : ""}>
  <div id="inner">
    <h2>Loading simplification</h2>
    <div class="spinner">
      <Jumper />
    </div>
    <h3>This may take some time</h3>
    <span>Current status: {status}</span>
  </div>
</main>

<style>
  .hidden {
    display: none;
  }
  main {
    position: absolute;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
  }
  #inner {
    padding: 20px;
    position: absolute;
    background: white;
    border-radius: 2px;
    width: fit-content;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  .spinner {
    width: fit-content;
    margin: 0 auto;
  }
</style>
