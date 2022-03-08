<script>
  export let points;
</script>

<main>
  {#each points as { point, level }, i}
    <li class={level}>{point}</li>
  {/each}
</main>

<style>
  li {
    text-align: left;
    list-style-type: none;
    padding: 10px;
    margin: 4px;
    background: #ffcccc;
    border: 1px solid;
    border-radius: 5px;
  }

  .critical {
    background: #ffaaaa;
    border-color: #ff7777;
  }
  .warn {
    background: #ffff77;
    border-color: #aaaa55;
  }
  .neutral {
    background: #cccccc;
    border-color: #aaaaaa;
  }
  .good {
    background: #7e7;
    border-color: #2a2;
  }
</style>
