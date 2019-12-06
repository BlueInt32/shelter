<template>
  <div class="addThingy">
    <div class="pure-g">
      <div class="pure-u-1-5"></div>
      <div class="pure-u-3-5">
        <h1>Add stuff</h1>
        <form class="pure-form pure-form-aligned">
          <fieldset>
            <legend>
              A "thingy" is something you just want to review later. <br />
              Who knows ? Maybe it would be a gem ?
            </legend>
            <div class="pure-control-group">
              <label for="name">Link, text, anything...</label>
              <input id="name" type="text" placeholder="" />
              <span class="pure-form-message-inline">Mandatory</span>
            </div>
            <div class="pure-control-group">
              <label for="name">Name (optional)</label>
              <input id="name" type="text" placeholder="" />
            </div>
            <div class="pure-controls">
              <button
                class="pure-button pure-button-primary"
                type="button"
                value="Add"
              >
                Add
              </button>
            </div>
          </fieldset>
        </form>
      </div>
      <div class="pure-u-1-5"></div>
    </div>
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  components: {}
})
export default class AddThingy extends Vue {
  created() {}
}
</script>
