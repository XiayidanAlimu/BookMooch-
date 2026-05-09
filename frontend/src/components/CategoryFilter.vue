<template>
  <a-card class="filter-card" size="small">
    <a-form layout="inline">
      <a-form-item label="书籍分类">
        <a-select
          v-model="selectedValue"
          placeholder="请选择分类"
          style="width: 200px;"
          @change="handleChange"
        >
          <a-option :value="0">全部分类</a-option>
          <a-option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </a-option>
        </a-select>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
  selectedCategoryId: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['category-change'])

const selectedValue = computed(() => props.selectedCategoryId || 0)

const handleChange = (value) => {
  emit('category-change', value === 0 ? null : value)
}
</script>

<style scoped>
.filter-card {
  margin-bottom: 16px;
}
</style>
