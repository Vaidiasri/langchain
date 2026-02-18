from reportlab.pdfgen import canvas


def create_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Retrieval-Augmented Generation (RAG)")
    c.drawString(100, 730, "RAG combines LLMs with external data retrieval.")
    c.drawString(100, 710, "Key components: Retrieval, Augmentation, Generation.")
    c.drawString(
        100, 690, "LangChain supports RAG via Document Loaders (like PyPDFLoader)."
    )
    c.save()


if __name__ == "__main__":
    create_pdf("dummy.pdf")
    print("dummy.pdf created successfully.")
