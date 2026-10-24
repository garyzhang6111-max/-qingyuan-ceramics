import Foundation
import PDFKit
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else {
    print("用法: swift pdf2img.swift <pdf路径> <输出目录>")
    exit(1)
}
let pdfPath = args[1]
let outDir = args[2]

guard let doc = PDFDocument(url: URL(fileURLWithPath: pdfPath)) else {
    print("无法打开 PDF")
    exit(1)
}
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)

let pageCount = doc.pageCount
print("页数: \(pageCount)")

for i in 0..<pageCount {
    guard let page = doc.page(at: i) else { continue }
    let bounds = page.bounds(for: .mediaBox)
    let scale: CGFloat = 1.6
    let size = CGSize(width: bounds.width * scale, height: bounds.height * scale)
    let img = NSImage(size: size)
    img.lockFocus()
    NSColor.white.setFill()
    NSRect(origin: .zero, size: size).fill()
    guard let ctx = NSGraphicsContext.current?.cgContext else { img.unlockFocus(); continue }
    ctx.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: ctx)
    img.unlockFocus()
    guard let tiff = img.tiffRepresentation,
          let rep = NSBitmapImageRep(data: tiff),
          let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.8]) else { continue }
    let outPath = "\(outDir)/page-\(String(format: "%03d", i+1)).jpg"
    try? data.write(to: URL(fileURLWithPath: outPath))
}
print("转换完成")
