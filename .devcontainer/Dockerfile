FROM docker.io/library/archlinux:base-20261011.0.609700@sha256:3c64b538588416593f69a1aebd2f2ec0f2541b29159f32556fa7def2167147a0

# Arch Linux Archive snapshot with the host toolchain versions; librsvg 2.63.2-1 reached extra after it, so it comes from the package archive.
RUN echo 'Server = https://archive.archlinux.org/repos/2026/10/01/$repo/os/$arch' > /etc/pacman.d/mirrorlist \
 && pacman -Syyuu --noconfirm \
 && pacman -S --noconfirm --needed python python-fonttools imagemagick cairo fontconfig ttf-fira-sans git \
 && pacman -U --noconfirm 'https://archive.archlinux.org/packages/l/librsvg/librsvg-2%3A2.63.2-1-x86_64.pkg.tar.zst' \
 && pacman -Scc --noconfirm \
 && test "$(pacman -Q imagemagick librsvg cairo python python-fonttools ttf-fira-sans fontconfig | tr '\n' ' ')" = "imagemagick 7.1.2.32-1 librsvg 2:2.63.2-1 cairo 1.18.6-1 python 3.14.7-1 python-fonttools 4.66.1-1 ttf-fira-sans 1:4.301-3 fontconfig 2:2.18.3-2 " \
 && test "$(ldd /usr/bin/rsvg-convert | grep -c 'not found')" = 0 \
 && rsvg-convert --version && magick -version \
 && useradd -m -u 1000 dev

USER dev
