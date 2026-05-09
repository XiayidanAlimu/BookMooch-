<template>
  <div class="max-w-6xl mx-auto p-6">
    <div class="bg-white rounded-xl shadow-sm p-8">
      <h2 class="text-3xl font-bold text-gray-900 mb-6">帮助中心</h2>
      <p class="text-gray-600 mb-6">
        这里简单介绍本平台的使用流程，帮助新手用户快速完成捐赠与领取。
      </p>

      <div class="space-y-8">
        <section class="rounded-3xl border border-gray-100 bg-gray-50 p-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-4">捐赠流程</h3>
          <ol class="space-y-4 list-decimal list-inside text-gray-700">
            <li>登录或注册账号。</li>
            <li>进入首页，点击“我要捐书”打开捐书表单。</li>
            <li>输入书名，系统可从公共图书数据库搜索匹配结果，直接选择图书信息。</li>
            <li>如果没有匹配项，可点击新增数据详情补充作者、ISBN、分类和简介。</li>
            <li>确认信息无误后提交，您的书籍将展示在平台中，供其他用户查看。</li>
          </ol>
        </section>

        <section class="rounded-3xl border border-gray-100 bg-gray-50 p-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-4">领取流程</h3>
          <ol class="space-y-4 list-decimal list-inside text-gray-700">
            <li>登录账号后进入图书列表页面。</li>
            <li>您可以直接领取想要的图书，也可以先添加到心愿单，稍后再处理。</li>
            <li>直接领取时，点击图书右侧“直接领取”按钮，填写邮寄信息并提交订单。</li>
            <li>订单提交后，可在“领取订单”页面查看订单状态和收货信息。</li>
            <li>如果不再想要某本心愿单图书，可进入“我的心愿单”页面将其移除。</li>
          </ol>
        </section>

        <section class="rounded-3xl border border-gray-100 bg-gray-50 p-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-4">常见问题</h3>
          <div class="space-y-4 text-gray-700">
            <div>
              <p class="font-semibold">Q1: 我可以领取自己的捐赠书籍吗？</p>
              <p>不支持领取自己的捐赠图书，系统会阻止此操作。</p>
            </div>
            <div>
              <p class="font-semibold">Q2: 如何查看我曾经提交的订单？</p>
              <p>登录后进入“领取订单”页面即可查看个人订单记录。</p>
            </div>
            <div>
              <p class="font-semibold">Q3: 心愿单能保存多久？</p>
              <p>心愿单会一直保存在您的账号下，直到您手动移除书籍。</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
</style>