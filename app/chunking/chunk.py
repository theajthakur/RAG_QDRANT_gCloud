from markdown_it import MarkdownIt
from dataclasses import dataclass

@dataclass
class Chunk:
    source: str
    path: list[str]
    text: str
    chunk_index: int

md = MarkdownIt()

files = [
    "family.md",
    "personal.md",
    "technical.md",
    "about_me.md",
    "biography.md",
]

base_path = "C:/Users/VIJAY/Documents/Projects/private/personal_knowledge_base/"

MAX_CHARS = 1500

all_chunks: list[Chunk] = []

def processChunks():
    chunk_index = 1

    for source in files:

        with open(base_path + source, encoding="utf-8") as f:
            text = f.read()

        tokens = md.parse(text)

        sections = []

        heading_stack = []
        current_content = []

        i = 0

        while i < len(tokens):

            token = tokens[i]

            if token.type == "heading_open":

                # Save previous section
                if heading_stack:
                    sections.append({
                        "path": heading_stack.copy(),
                        "content": "\n".join(current_content).strip()
                    })

                current_content = []

                level = int(token.tag[1])
                heading = tokens[i + 1].content

                heading_stack = heading_stack[: level - 1]
                heading_stack.append(heading)

                i += 3
                continue

            elif token.type == "inline":
                current_content.append(token.content)

            i += 1

        # Save final section
        if heading_stack:
            sections.append({
                "path": heading_stack.copy(),
                "content": "\n".join(current_content).strip()
            })

        # Create chunks
        for section in sections:

            # Split by paragraphs if possible
            paragraphs = (
                section["content"].split("\n\n")
                if "\n\n" in section["content"]
                else [section["content"]]
            )

            current = ""

            for para in paragraphs:

                if len(current) + len(para) > MAX_CHARS and current:

                    all_chunks.append(
                        Chunk(
                            source=source,
                            path=section["path"],
                            text=current.strip(),
                            chunk_index=chunk_index,
                        )
                    )

                    chunk_index += 1
                    current = para

                else:
                    current += ("\n\n" if current else "") + para

            if current.strip():
                all_chunks.append(
                    Chunk(
                        source=source,
                        path=section["path"],
                        text=current.strip(),
                        chunk_index=chunk_index,
                    )
                )
                chunk_index += 1

def getAllChunks() -> list[Chunk]:
    processChunks()
    return all_chunks