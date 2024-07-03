from googletrans import Translator

translator = Translator()
t1 = translator.translate(
    "The Max Planck Institute for Ornithology was a non-university research institution under the sponsorship of the Max Planck Society for the Advancement of Science (MPG). As of January 1st 2023, it merged with the Max Planck Institute for Neurobiology to form the new Max Planck Institute for Biological Intelligence. The institute is located in Seewiesen, which belongs to the municipality of Pöcking in Upper Bavaria. The institute’s focus was on basic scientific research in the fields of organismic biology, zoology, ornithology, neurobiology, behavioural ecology, evolutionary biology and evolutionary genetics. The institute is managed on a collegial basis, i.e. one of the two directors of the institute takes over the management for a certain time period.",
    src="en",
    dest="es",
).text
t2 = translator.translate(t1, src="es", dest="nl").text
t3 = translator.translate(t2, src="nl", dest="en").text
print(t3)
