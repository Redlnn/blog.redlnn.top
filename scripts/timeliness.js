// https://hexo.fluid-dev.com/posts/hexo-injector/

hexo.extend.injector.register('body_end', `
  <script defer src="/js/timeliness.js"></script>
`);
