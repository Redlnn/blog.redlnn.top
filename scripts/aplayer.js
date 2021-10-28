// https://hexo.fluid-dev.com/posts/hexo-injector/

hexo.extend.injector.register(
  'body_end',
  `<div id="aplayer"></div>
   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aplayer@1/dist/APlayer.min.css">
   <script src="https://cdn.jsdelivr.net/npm/aplayer@1/dist/APlayer.min.js"></script>
   <script src="https://cdn.jsdelivr.net/npm/meting@2/dist/Meting.min.js"></script>
   <meting-js
     server="netease"
     type="playlist"
     id="6673512356"
     autoplay="true"
     loop="all"
     fixed="true"
     order="random">
   </meting-js>`
)
