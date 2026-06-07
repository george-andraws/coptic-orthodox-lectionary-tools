import Foundation
import PDFKit
import Vision
import AppKit

func renderPage(_ page: PDFPage, scale: CGFloat = 2.0) -> CGImage? {
    let bounds = page.bounds(for: .mediaBox)
    let width = Int(bounds.width * scale)
    let height = Int(bounds.height * scale)
    guard let colorSpace = CGColorSpace(name: CGColorSpace.sRGB),
          let ctx = CGContext(data: nil, width: width, height: height, bitsPerComponent: 8, bytesPerRow: 0, space: colorSpace, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)
    else { return nil }
    ctx.setFillColor(NSColor.white.cgColor)
    ctx.fill(CGRect(x: 0, y: 0, width: width, height: height))
    ctx.saveGState()
    ctx.translateBy(x: 0, y: CGFloat(height))
    ctx.scaleBy(x: scale, y: -scale)
    page.draw(with: .mediaBox, to: ctx)
    ctx.restoreGState()
    return ctx.makeImage()
}

let args = CommandLine.arguments
guard args.count >= 3 else {
    fputs("usage: swift ocr_pdf_vision.swift input.pdf output.txt [startPage] [endPage]\n", stderr)
    exit(1)
}
let input = args[1]
let output = args[2]
let startPage = args.count >= 4 ? max(1, Int(args[3]) ?? 1) : 1
let endPageArg = args.count >= 5 ? Int(args[4]) : nil

guard let doc = PDFDocument(url: URL(fileURLWithPath: input)) else {
    fputs("failed to open pdf\n", stderr)
    exit(1)
}
let endPage = min(doc.pageCount, endPageArg ?? doc.pageCount)
var out = ""
for i in startPage...endPage {
    guard let page = doc.page(at: i - 1), let image = renderPage(page) else { continue }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    req.recognitionLanguages = ["ar", "en-US"]
    let handler = VNImageRequestHandler(cgImage: image, options: [:])
    do {
        try handler.perform([req])
        out += "\n===== PAGE \(i) =====\n"
        let obs = req.results ?? []
        for o in obs {
            if let top = o.topCandidates(1).first {
                out += top.string + "\n"
            }
        }
    } catch {
        out += "\n===== PAGE \(i) OCR ERROR: \(error) =====\n"
    }
}
try out.write(to: URL(fileURLWithPath: output), atomically: true, encoding: .utf8)
print("wrote", output)
