import Messages
import UIKit

final class MessagesViewController: MSMessagesAppViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        embedStickerBrowser()
    }

    private func embedStickerBrowser() {
        let browser = StickerBrowserViewController(stickerSize: .regular)
        addChild(browser)
        browser.view.frame = view.bounds
        browser.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(browser.view)
        browser.didMove(toParent: self)
    }
}

final class StickerBrowserViewController: MSStickerBrowserViewController {
    private let stickers: [MSSticker] = StickerBrowserViewController.loadStickers()

    override func numberOfStickers(in stickerBrowserView: MSStickerBrowserView) -> Int {
        stickers.count
    }

    override func stickerBrowserView(_ stickerBrowserView: MSStickerBrowserView, stickerAt index: Int) -> MSSticker {
        stickers[index]
    }

    private static func loadStickers() -> [MSSticker] {
        let items: [(file: String, label: String)] = [
            ("Sticker1", "Mari Summers conference badge"),
            ("Sticker2", "Mari Summers"),
            ("Sticker3", "Mari Summers looking back"),
        ]
        return items.compactMap { item in
            guard let url = Bundle.main.url(forResource: item.file, withExtension: "png") else {
                return nil
            }
            return try? MSSticker(contentsOfFileURL: url, localizedDescription: item.label)
        }
    }
}
