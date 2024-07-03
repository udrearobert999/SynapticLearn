from dialogs_generation_utils import generate_dialogs
from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Yi-6B-200K-GGUF",
    model_file="yi-6b-200k.Q4_K_M.gguf",
    model_type="yi",
    gpu_layers=50,
)

text = "The Beijing Anomaly is an observed seismic feature in the Earth's mantle at a depth of around 700–1400 km below Northeastern China where a high degree of seismic attenuation was discovered to exist. According to its discoverers, Jesse Lawrence (from Scripps Institute of Oceanography) and Michael Wysession (from Washington University), the Beijing Anomaly is evidence for large amounts of water contained within the mantle. The effects of water on the attenuation of seismic waves are largely unknown, although theoretical expectations seem to indicate that a seismic Q·¹ factor change from 300 to 100 can be explained by an approximate tenfold increase in water content. This leads to the hypothesis that only small amounts of water, present at depth within the mantle (on the order of 0.1 wt%), will lead to significant seismic attenuation and could potentially explain the anomalously low Q·¹ values which extend over a broad region in the mantle below Northeast Asia.The zone of low Q·¹ existing in the mantle below Northeastern China was found via seismic attenuation tomography and begins approximately 700 km below the surface and displays stark decreases in Q·¹ values, down to a minimum of Q·¹= 95 at around 1000 km in depth. The extent of the anomaly below a large portion of Northeast Asia would require the existence of contributing factors which would facilitate the distribution of water within the mantle itself. Factors which could facilitate the dispersion of water to such a degree include mantle-rock advection and water transport along grain boundaries.It has therefore been suggested that the downgoing oceanic lithosphere can carry with it large amounts of water into deeper regions of the mantle, directly below the continental margins (to depths reaching far beyond 1400 km). The water contained within these subducting slabs is thought to remain unaffected by the surrounding high-temperature and pressure conditions, since it is contained within the centre of the cold lithospheric slab. The seismic attenuation anomalies in Northeast China are potentially explained by water having been extracted from the cold, deep-seated oceanic lithosphere and “flooding” the overlying lower mantle wedge at depth, giving rise to zones of high elasticity (and potentially fluid-rich) which would cause levels of seismic attenuation that were observed tomographically.Recent research has been able to better constrain the degree to which subducting oceanic mantle is hydrated using measurements of P-wave attenuation from localized earthquakes near the Wadati–Benioff zone. Estimates suggest an approximately 40 km thick layer of moderately serpentinized mantle would be sufficient to explain the observed seismic P-wave attenuations associated to events occurring at depths of around 5–35 km below the Wadati–Benioff zone. This would imply that the topmost zones of the oceanic lithosphere provide a significant source of water to deeper areas of the mantle during subduction, with an estimated flux of 170-318 Tg/ma of water per meter of down-going slab. "
chunks = generate_dialogs(llm, [text], "paragraphs", max_tokens=512)
for dialog in chunks:
    dialog_responses = []
    for paragraph in dialog:
        rephrased_paragraph = llm(paragraph)
        dialog_responses.append(rephrased_paragraph)

    dialog_responses = " ".join(dialog_responses)
    print(dialog_responses)
