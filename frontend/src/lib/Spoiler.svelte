<script>
    let show = false;

    function switchSpoiler() {
        show = !show;
    }

    export let length;
    export let threshold;
</script>

<main>
    <div class="spoiler">
        <button on:click={switchSpoiler}>Advanced Options ></button>
    </div>
    {#if show}
        <div class="content">
            <label for="length_slider">Abstractive Summary Length:</label>
            <input
                bind:value={length}
                type="range"
                min="10"
                max="100"
                step="5"
                class="slider"
                id="length_slider"
                name="length_slider"
            />
            <output>{length}%</output>
            <br />
            <label for="threshold_slider">Extractive Threshold:</label>
            <input
                bind:value={threshold}
                type="range"
                min="0.4"
                max="0.9"
                step="0.025"
                class="slider"
                id="threshold_slider"
                name="threshold_slider"
            />
            <output>{threshold}</output>
        </div>
    {/if}
</main>

<style>
    .spoiler button {
        border: none;
        background: none;
        padding: 10px;
        cursor: pointer;
    }

    .content * {
        accent-color: var(--colour-accent);
    }

    .content {
        font-size: 0.8em;
        line-height: 2em;
        width: fit-content;
        margin: auto;
        text-align: left;
        padding: 0 0 20px 0;
    }
</style>
