# Kindred Spirit: Building an LLM that follows personal ethics

<table>
<tr>
<td width="50%">
<img src="aristotle_with_a_bust_of_homer-Rembrandt1653.jpeg" alt="Aristotle with a Bust of Homer by Rembrandt (1653)" width="100%">
<br><sub><sup>Aristotle with a Bust of Homer - Rembrandt (1653)</sup></sub>
</td>
<td width="50%" valign="middle">
<h3><a href="https://en.wikipedia.org/wiki/Aristotle">Aristotle</a> (384-322 BCE)</h3>
<blockquote>
<p><em>"We are what we repeatedly do. Excellence, then, is not an act, but a habit."</em></p>
</blockquote>
<br>
<h3><a href="https://en.wikipedia.org/wiki/George_Orwell">George Orwell</a> (1903-1950)</h3>
<blockquote>
<p><em>"Who controls the past controls the future. Who controls the present controls the past."</em></p>
</blockquote>
<br>
<h3><a href="https://en.wikipedia.org/wiki/Hannah_Arendt">Hannah Arendt</a> (1906-1975)</h3>
<blockquote>
<p><em>"The sad truth is that most evil is done by people who never make up their minds to be good or evil."</em></p>
</blockquote>
</td>
</tr>
</table>

---

# Kindred Spirit: The Sovereign Ethics Layer

# Kindred Spirit: The Sovereign Ethics Layer

> "I am building this so my daughters have an AI that reflects the nuance of history and the weight of personal conscience, rather than the sterilized safety-tuning of a corporation."

## 🚀 The Mission
**Kindred Spirit** is an experimental framework for personalizing the moral and ethical foundations of Large Language Models. 

Standard LLMs are "Thin Clients" for centralized, corporate ethics. Kindred Spirit moves the "Moral Processing" back to the individual. By fine-tuning a model on a curated set of 70+ personal ethical dilemmas, we create a **Sovereign Intelligence**—an AI that acts as a true "Kindred Spirit" to its creator.

## 🏗 System Architecture

Kindred Spirit uses a **LoRA (Low-Rank Adaptation)** approach to "overlay" a personal ethical framework onto a neutral base model.

```mermaid
graph TD
    A[Global Information] --> B{Centralized LLM}
    B --> C[Standard User]
    D[Neutral Base Model] --> E[Nigel Ethics LoRA]
    E --> F[The Family]
    B -.-> E


Base Model: Qwen2.5-7B (Abliterated)

Adapter: LoRA (Rank 64 / Alpha 128)

Hardware: NVIDIA RTX 6000 Ada (48GB VRAM)

Framework: Unsloth / HuggingFace PEFT

Context: Fine-tuned on a proprietary dataset of 74 high-stakes moral dilemmas.

📚 Core Philosophies
The model is grounded in three primary invariants:

Hannah Arendt: Recognizing and resisting the "Banality of Evil."

George Orwell: Protecting the "Ground Truth" from linguistic and historical drift.

The Fat Client: Maintaining technical and moral sovereignty at the local node.

📂 Project Structure
/data: The ethical scenarios used for SFT.

/models: Configuration for the LoRA adapter.

LLM_PersonalEthics.md: The philosophical "Source Code" of the project.

Created by Nigel Burton, 2026. A tool for the next generation.