import './styles.scss';
// アンカー(a)があれば、Buttonコンポーネントを描画
if (document.querySelectorAll('a').length) {
    require.ensure([], () => {
        const Button = require('./Components/Button').default;
        const button = new Button('google.com');
        button.render('a');
    });
}
// タイトル(h1)があれば、Headerコンポーネントを描画
if (document.querySelectorAll('h1').length) {
    require.ensure([], () => {
        const Header = require('./Components/Header').default;
        new Header().render('h1');
    });
}
