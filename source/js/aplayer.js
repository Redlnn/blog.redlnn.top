// https://hexo.fluid-dev.com/posts/hexo-injector/
// https://aplayer.js.org/#/zh-Hans/?id=%E5%8F%82%E6%95%B0

!(function () {
    var oldLoadAp = window.onload;
    window.onload = function () {
        oldLoadAp && oldLoadAp();

        new APlayer({
            container: document.getElementById("aplayer"),
            fixed: true,
            autoplay: false,
            loop: "all",
            order: "random",
            theme: "#b7daff",
            preload: "auto",
            audio: [
                {
                    name: "song1",
                    artist: "artist1",
                    url: "/songs/song1.mp3",
                    cover: "/img/cover.jpg",
                },
            ],
        });
    };
})();
