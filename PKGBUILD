# Maintainer: davidykmisha2015-prog

pkgname=boxer
pkgver=1.1.1
pkgrel=1
pkgdesc="A lightweight, blazing-fast manager for isolated development environments"
arch=('x86_64')
url="https://github.com/davidykmisha2015-prog/Boxer"
license=('MIT')
depends=('glibc')
# Замініть URL, якщо ваш архів має іншу назву або лежить за іншим посиланням
source=("${url}/releases/download/v${pkgver}/Boxer-Linux-x86_64.tar.gz")
sha256sums=('SKIP')

package() {
    # Встановлюємо CLI та UI версії
    install -Dm755 "${srcdir}/boxer" "${pkgdir}/usr/bin/boxer"
    install -Dm755 "${srcdir}/boxer_app" "${pkgdir}/usr/bin/boxer_app"

    # Встановлюємо іконку
    install -Dm644 "${srcdir}/app_icon.png" "${pkgdir}/usr/share/pixmaps/boxer.png"

    # Встановлюємо ярлик
    install -Dm644 "${srcdir}/boxer_app.desktop" "${pkgdir}/usr/share/applications/boxer.desktop"

    # Оновлюємо шляхи в ярлику, щоб вони відповідали системним
    sed -i "s|Exec=.*|Exec=/usr/bin/boxer_app|" "${pkgdir}/usr/share/applications/boxer.desktop"
    sed -i "s|Icon=.*|Icon=boxer|" "${pkgdir}/usr/share/applications/boxer.desktop"
}
