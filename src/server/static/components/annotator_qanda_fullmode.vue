<template lang="pug">
  div(@click="setSelectedRange")
    span.text-sequence(
      oncopy="return false"
      oncut="return false"
      v-for="r in chunks"
      v-bind:class="getChunkClass(r)"
      v-bind:style="getChunkStyle(r)"
    ) {{ textPart(r) }}
      button.delete.is-small(v-if="r.label==1", v-on:click="removeAnswer(r)")
</template>

<script>
import Bus from './bus.js'

export default {
  props: {
    text: {
      type: String,
      default: '',
    },
    entityPositions: {
      type: Array, // [{'startOffset': 10, 'endOffset': 15, 'label_id': 1}]
      default: () => [],
    },
  },

  data: () => ({
    startOffset: 0,
    endOffset: 0,
    editMode: false,
  }),

  computed: {
    entityPositionsOrempty() {
      return (this.editMode) ? [] : this.entityPositions;
    },

    sortedEntityPositions() {
      /* eslint-disable vue/no-side-effects-in-computed-properties */
      return this.entityPositionsOrempty.sort((a, b) => a.start_offset - b.start_offset);
      /* eslint-enable vue/no-side-effects-in-computed-properties */
    },

    chunks() {
      const res = [];
      let left = 0;
      let e;
      for (let i = 0; i < this.sortedEntityPositions.length; i++) {
        e = this.sortedEntityPositions[i];
        e.label = 1;
        e.end_offset = e.start_offset + e.response.length;

        const l = this.makeEmptyChunk(left, e.start_offset);

        res.push(l);
        res.push(e);
        left = e.end_offset;
      }
      const l = this.makeEmptyChunk(left, this.text.length);
      res.push(l);

      return res;
    },

  },

  watch: {
    entityPositions() {
      this.resetRange();
    },
  },

  methods: {
    getChunkClass(chunk) {
      if (chunk.label === 0) {
        return {};
      }
      return [
        { tag: '#ffffff' },
      ];
    },

    getChunkStyle(chunk) {
      if (chunk.label === 0) {
        return {};
      }
      return {
        color: '#ffffff',
        backgroundColor: '#4169e1',
      };
    },


    setSelectedRange() {
      let start;
      let end;
      if (window.getSelection) {
        const range = window.getSelection().getRangeAt(0);
        const preSelectionRange = range.cloneRange();
        preSelectionRange.selectNodeContents(this.$el);
        preSelectionRange.setEnd(range.startContainer, range.startOffset);
        start = [...preSelectionRange.toString()].length;
        end = start + [...range.toString()].length;
      } else if (document.selection && document.selection.type !== 'Control') {
        const selectedTextRange = document.selection.createRange();
        const preSelectionTextRange = document.body.createTextRange();
        preSelectionTextRange.moveToElementText(this.$el);
        preSelectionTextRange.setEndPoint('EndToStart', selectedTextRange);
        start = [...preSelectionTextRange.text].length;
        end = start + [...selectedTextRange.text].length;
      }
      this.startOffset = start;
      this.endOffset = end;
      // console.log(start, end); // eslint-disable-line no-console
    },

    validRange() {
      if (this.startOffset === this.endOffset) {
        return false;
      }
      if (this.startOffset > this.text.length || this.endOffset > this.text.length) {
        return false;
      }
      if (this.startOffset < 0 || this.endOffset < 0) {
        return false;
      }
      for (let i = 0; i < this.entityPositionsOrempty.length; i++) {
        const e = this.entityPositionsOrempty[i];
        if ((e.start_offset <= this.startOffset) && (this.startOffset < e.end_offset)) {
          return false;
        }
        if ((e.start_offset < this.endOffset) && (this.endOffset < e.end_offset)) {
          return false;
        }
        if ((this.startOffset < e.start_offset) && (e.start_offset < this.endOffset)) {
          return false;
        }
        if ((this.startOffset < e.end_offset) && (e.end_offset < this.endOffset)) {
          return false;
        }
      }
      return true;
    },

    hasAnswer() {
      if (this.entityPositionsOrempty.length > 0) {
        return true;
      }
      return false;
    },

    resetRange() {
      this.startOffset = 0;
      this.endOffset = 0;
    },

    textPart(r) {
      return [...this.text].slice(r.start_offset, r.end_offset).join('');
    },

    addAnswer() {
      if (this.validRange() && !this.hasAnswer()) {
        const text = {
          start_offset: this.startOffset,
          response: [...this.text].slice(this.startOffset, this.endOffset).join(''),
        };
        Bus.$emit('addAnswer-with-text',text)
      }
    },

    removeAnswer(index) {
      Bus.$emit('clicked-on-removeAnswer')
    },

    makeEmptyChunk(startOffset, endOffset) {
      const chunk = {
        id: 0,
        label: 0,
        start_offset: startOffset,
        end_offset: endOffset,
      };
      return chunk;
    },
  },

  created() {
    Bus.$on('clicked-on-addAnswer', () => {
        this.addAnswer()
    });
    Bus.$on('switch-editmode', (boo) => {
        this.editMode = boo
    });
    window.addEventListener("touchend", () => { this.setSelectedRange() });
    document.addEventListener("selectionchange", () => { this.setSelectedRange() });
  },

};
</script>
