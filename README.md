<img alt="My Logo" class="logo header-image only-light align-center" src="https://storage.googleapis.com/storage.khchao.com/figures/LiftOn/LiftOn_color.png" style="width:90%">

<div class="content">
<a class="reference external image-reference" href="https://img.shields.io/badge/License-GPLv3-yellow.svg"><img alt="https://img.shields.io/badge/License-GPLv3-yellow.svg" src="https://img.shields.io/badge/License-GPLv3-yellow.svg"></a>
<a class="reference external image-reference" href="https://img.shields.io/badge/version-v.0.0.1-blue"><img alt="https://img.shields.io/badge/version-v.0.0.1-blue" src="https://img.shields.io/badge/version-v.1.0.0-blue"></a>
<a class="reference external image-reference" href="https://pepy.tech/project/lifton"><img alt="https://static.pepy.tech/personalized-badge/lifton?period=total&amp;units=abbreviation&amp;left_color=grey&amp;right_color=blue&amp;left_text=PyPi%20downloads" src="https://static.pepy.tech/personalized-badge/lifton?period=total&amp;units=abbreviation&amp;left_color=grey&amp;right_color=blue&amp;left_text=PyPi%20downloads"></a>
<a class="reference external image-reference" href="https://github.com/Kuanhao-Chao/lifton/releases"><img alt="https://img.shields.io/github/downloads/Kuanhao-Chao/lifton/total.svg?style=social&amp;logo=github&amp;label=Download" src="https://img.shields.io/github/downloads/Kuanhao-Chao/lifton/total.svg?style=social&amp;logo=github&amp;label=Download"></a>
<a class="reference external image-reference" href="https://github.com/Kuanhao-Chao/lifton/releases"><img alt="https://img.shields.io/badge/platform-macOS_/Linux-green.svg" src="https://img.shields.io/badge/platform-macOS_/Linux-green.svg"></a>
<a class="reference external image-reference" href="https://colab.research.google.com/github/Kuanhao-Chao/lifton/blob/main/notebook/lifton_example.ipynb"><img alt="https://colab.research.google.com/assets/colab-badge.svg" src="https://colab.research.google.com/assets/colab-badge.svg"></a>
<div class="line-block">
<div class="line"><br></div>
</div>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

LiftOn is a homology-based lift-over tool using both DNA-DNA alignments (from <a href="https://academic.oup.com/bioinformatics/article/37/12/1639/6035128?login=true" target="_blank">Liftoff</a>, credits to <a href="https://scholar.google.com/citations?user=N3tXk7QAAAAJ&amp;hl=en" target="_blank">Dr. Alaina Shumate</a>) and protein-DNA alignments (from <a href="https://academic.oup.com/bioinformatics/article/39/1/btad014/6989621" target="_blank">miniprot</a>, credits to <a href="http://liheng.org" target="_blank">Dr. Heng Li</a>) to accurately map annotations between genome assemblies of the same or different species. LiftOn employs a two-step <a href="https://ccb.jhu.edu/lifton/content/behind_scenes.html#protein-maximization-algorithm">protein maximization algorithm</a> to improve the annotation of protein-coding genes in the T2T-CHM13 <a href="https://s3-us-west-2.amazonaws.com/human-pangenomics/T2T/CHM13/assemblies/annotation/chm13v2.0_RefSeq_Liftoff_v5.1.gff3.gz" target="_blank">JHU RefSeqv110 + Liftoff v5.1</a> annotation.
The latest T2T-CHM13 annotation generated by LiftOn is available as <a href="https://tinyurl.com/4xywtwve" target="_blank">JHU_LiftOn_v1.0_chm13v2.0.gff3 (ftp://ftp.ccb.jhu.edu/pub/data/LiftOn/JHU_LiftOn_v1.0_chm13v2.0.gff3) <i class="fa fa-download"></i></a>.<section id="why-lifton" class="">
<h2>Why LiftOn❓<a class="headerlink" href="#why-lifton" title="Permalink to this heading">#</a></h2>
<ol class="arabic simple">
<li><p><strong>Burgeoning number of genome assemblies</strong>: As of December 2023, there are 30,530 eukaryotic genomes, 567,228 prokaryotic genomes, and 66,429 viruses listed on NCBI (<a class="reference external" href="https://www.ncbi.nlm.nih.gov/genome/browse/#!/overview/">NCBI genome browser</a>). However, genome annotation is lagging behind. As more high-quality assemblies are generated, we need an accurate lift-over tool to annotate them.</p></li>
<li><p><strong>Improved protein-coding gene mapping</strong>: The popular <a class="reference external" href="https://academic.oup.com/bioinformatics/article/37/12/1639/6035128?login=true">Liftoff</a> tool maps genes based on DNA alignments alone. <a class="reference external" href="https://github.com/lh3/miniprot">Miniprot</a> maps genes based on protein alignments but, without gene structure information, may not be as accurate on their own (See <a class="reference internal" href="https://ccb.jhu.edu/lifton/content/how_to_page.html#why-lifton-qa"><span class="std std-ref">FAQ Common mistakes of Liftoff and miniprot</span></a>). LiftOn combines both DNA-to-genome and protein-to-genome alignments and produces better gene mapping results! LiftOn improves upon the current released T2T-CHM13 annotation (<a class="reference external" href="https://s3-us-west-2.amazonaws.com/human-pangenomics/T2T/CHM13/assemblies/annotation/chm13v2.0_RefSeq_Liftoff_v5.1.gff3.gz">JHU RefSeqv110 + Liftoff v5.1</a>).</p></li>
<li><p><strong>Improved distantly related species lift-over</strong>: A key limitation of DNA-based lift-over tools is that they do not perform well when the reference and target genomes have significantly diverged. With the help of protein alignments and the protein maximization algorithm, LiftOn improves the lift-over process between distantly related species. See "<a class="reference internal" href="https://ccb.jhu.edu/lifton/content/distant_species_liftover/liftover_mouse_2_rat.html#distant-species-liftover-mouse-to-rat"><span class="std std-ref">Mouse to Rat</span></a>" and "<a class="reference internal" href="https://ccb.jhu.edu/lifton/content/distant_species_liftover/liftover_drosophila_erecta.html#distant-species-liftover-drosophila-melanogaster-2-erecta"><span class="std std-ref">Drosophila melanogaster to Drosophila erecta</span></a>" result sections.</p></li>
</ol>
<p>LiftOn is free, it's open source, it's easy to install , and it's in Python!</p>
<div class="line-block">
<div class="line"><br></div>
</div>
</section>
<section id="who-is-it-for" class="">
<h2>Who is it for❓<a class="headerlink" href="#who-is-it-for" title="Permalink to this heading">#</a></h2>
<p>LiftOn is designed for researchers and bioinformaticians who are interested in genome annotation. It is an easy-to-install and easy-to-run command-line tool. Specifically, it is beneficial in the following scenarios:</p>
<ol class="arabic simple">
<li><p>If you have sequenced and assembled a new genome and require annotation, LiftOn provides an efficient solution for generating annotations for your genome.</p></li>
<li><p>LiftOn is an excellent tool for those looking to perform comparative genomics analysis. It facilitates the lifting over and comparison of gene contents between different genomes, aiding in understanding evolutionary relationships and functional genomics.</p></li>
<li><p>For researchers interested in using T2T-CHM13 annotations, try LiftOn! We have pre-generated the <a class="reference external" href="https://tinyurl.com/4xywtwve">JHU_LiftOn_v1.0_chm13v2.0.gff3</a> (ftp://ftp.ccb.jhu.edu/pub/data/LiftOn/JHU_LiftOn_v1.0_chm13v2.0.gff3) file for your convenience.</p></li>
</ol>
<div class="line-block">
<div class="line"><br></div>
</div>
</section>
<section id="what-does-lifton-do" class="">
<h2>What does LiftOn do❓<a class="headerlink" href="#what-does-lifton-do" title="Permalink to this heading">#</a></h2>
<p>Let's first define the problem:
Given a reference <strong>Genome</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="0" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D445 TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>R</mi></math></mjx-assistive-mml></mjx-container></span>, an <strong>Annotation</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="1" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D445 TEX-I"></mjx-c></mjx-mi><mjx-script style="vertical-align: -0.153em;"><mjx-mi class="mjx-i" size="s"><mjx-c class="mjx-c1D434 TEX-I"></mjx-c></mjx-mi></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>R</mi><mi>A</mi></msub></math></mjx-assistive-mml></mjx-container></span>, and a target <strong>Genome</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="2" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D447 TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>T</mi></math></mjx-assistive-mml></mjx-container></span>. The lift-over problem is defined as the process of changing the coordinates of <strong>Annotation</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="3" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D445 TEX-I"></mjx-c></mjx-mi><mjx-script style="vertical-align: -0.153em;"><mjx-mi class="mjx-i" size="s"><mjx-c class="mjx-c1D434 TEX-I"></mjx-c></mjx-mi></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>R</mi><mi>A</mi></msub></math></mjx-assistive-mml></mjx-container></span> from <strong>Genome</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="4" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D445 TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>R</mi></math></mjx-assistive-mml></mjx-container></span> to <strong>Genome</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="5" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D447 TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>T</mi></math></mjx-assistive-mml></mjx-container></span>, and generate a new annotation file <strong>Annotation</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="6" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D447 TEX-I"></mjx-c></mjx-mi><mjx-script style="vertical-align: -0.153em; margin-left: -0.12em;"><mjx-mi class="mjx-i" size="s"><mjx-c class="mjx-c1D434 TEX-I"></mjx-c></mjx-mi></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>T</mi><mi>A</mi></msub></math></mjx-assistive-mml></mjx-container></span>. A simple illustration of the lift-over problem is shown in <a class="reference internal" href="#liftover-illustration"><span class="std std-numref">Figure 1</span></a>.</p>
<figure class="align-center" id="id4">
<figcaption>
<span id="liftover-illustration"></span><a class="reference internal image-reference" href="https://storage.googleapis.com/storage.khchao.com/figures/LiftOn/liftover_illustration.gif"><img alt="graphics/liftover_illustration.gif" src="https://storage.googleapis.com/storage.khchao.com/figures/LiftOn/liftover_illustration.gif" style="width: 672.5px; height: 270.0px;"></a>
</figcaption>
</figure>
<div class="line-block">
<div class="line"><br></div>
</div>
<p>LiftOn is the best tool to help you solve this problem! LiftOn employs a two-step <a class="reference internal" href="https://ccb.jhu.edu/lifton/content/behind_scenes.html#protein-maximization-algorithm"><span class="std std-ref">protein maximization algorithm</span></a> (PM algorithm).</p>
<ol class="arabic simple">
<li><p>The first module is the <em>chaining algorithm</em>. It starts by extracting protein sequences annotated by Liftoff and miniprot. LiftOn then aligns these sequences to full-length reference proteins. For each gene locus, LiftOn compares each section of the protein alignments from Liftoff and miniprot, chaining together the best combinations.</p></li>
<li><p>The second module is the <em>open-reading frame search (ORF search) algorithm</em>. In the case of truncated protein-coding transcripts, this algorithm examines alternative frames to identify the ORF that produces the longest match with the reference protein.</p></li>
</ol>
<div class="line-block">
<div class="line"><br></div>
</div>
</section>
<section id="inputs-outputs" class="">
<h2>Inputs &amp; outputs<a class="headerlink" href="#inputs-outputs" title="Permalink to this heading">#</a></h2>
<ul class="simple">
<li><dl class="simple">
<dt><strong>Input</strong>:</dt><dd><ol class="arabic simple">
<li><p>target <strong>Genome</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="7" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D447 TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>T</mi></math></mjx-assistive-mml></mjx-container></span> in FASTA format.</p></li>
<li><p>reference <strong>Genome</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="8" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D445 TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>R</mi></math></mjx-assistive-mml></mjx-container></span> in FASTA format.</p></li>
<li><p>reference <strong>Annotation</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="9" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D445 TEX-I"></mjx-c></mjx-mi><mjx-script style="vertical-align: -0.153em;"><mjx-mi class="mjx-i" size="s"><mjx-c class="mjx-c1D434 TEX-I"></mjx-c></mjx-mi></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>R</mi><mi>A</mi></msub></math></mjx-assistive-mml></mjx-container></span> in GFF3 format.</p></li>
</ol>
</dd>
</dl>
</li>
<li><dl class="simple">
<dt><strong>Output</strong>:</dt><dd><ol class="arabic simple">
<li><p>LiftOn annotation file, <strong>Annotation</strong> <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="10" style="font-size: 118.9%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D447 TEX-I"></mjx-c></mjx-mi><mjx-script style="vertical-align: -0.153em; margin-left: -0.12em;"><mjx-mi class="mjx-i" size="s"><mjx-c class="mjx-c1D434 TEX-I"></mjx-c></mjx-mi></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>T</mi><mi>A</mi></msub></math></mjx-assistive-mml></mjx-container></span>, in GFF3 format.</p></li>
<li><p>Protein sequence identities &amp; mutation types</p></li>
<li><p>Features with extra copies</p></li>
<li><p>Unmapped features</p></li>
</ol>
</dd>
</dl>
</li>
</ul>
<div class="line-block">
<div class="line"><br></div>
</div>
</section>
<section id="cite-us" class="">
<h2>Cite us<a class="headerlink" href="#cite-us" title="Permalink to this heading">#</a></h2>
<p>Kua-Hao Chao, Jakob M. Heinz, Celine Hoh, Alan Mao, Alaina Shumate, Mihaela Pertea, and Steven L. Salzberg. <i>"Combining DNA and protein alignments to improve genome annotation with LiftOn."</i> <b>bioRxiv coming soon</b>.
<a href="https://doi.org/10.1093/bioinformatics/btaa1016" target="_blank"> <svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15" class="icon outbound"><path fill="currentColor" d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path> <polygon fill="currentColor" points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg> </a> </p>

<p>Alaina Shumate, and Steven L. Salzberg. <i>"Liftoff: accurate mapping of gene annotations."</i> <b>Bioinformatics</b> 37.12 (2021): 1639-1643.

<a href="https://doi.org/10.1093/bioinformatics/btaa1016" target="_blank"> <svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15" class="icon outbound"><path fill="currentColor" d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path> <polygon fill="currentColor" points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg>
</a>
</p><div class="line-block">
<div class="line"><br></div>
</div>
</section>
<section id="user-support" class="">
<h2>User support<a class="headerlink" href="#user-support" title="Permalink to this heading">#</a></h2>
<p>Please go through the <a class="reference internal" href="#table-of-contents"><span class="std std-ref">documentation</span></a> below first. If you have questions about using the package, a bug report, or a feature request, please use the GitHub issue tracker here:</p>
<p><a class="reference external" href="https://github.com/Kuanhao-Chao/LiftOn/issues">https://github.com/Kuanhao-Chao/LiftOn/issues</a></p>
<div class="line-block">
<div class="line"><br></div>
</div>
</section>
<section id="key-contributors" class="">
<h2>Key contributors<a class="headerlink" href="#key-contributors" title="Permalink to this heading">#</a></h2>
<p>LiftOn was designed and developed by <a class="reference external" href="https://khchao.com/">Kuan-Hao Chao</a>.  This documentation was written by <a class="reference external" href="https://khchao.com/">Kuan-Hao Chao</a> and <a class="reference external" href="https://github.com/am12">Alan Man</a>. The LiftOn logo was designed by <a class="reference external" href="https://github.com/am12">Alan Man</a>.</p>
<div class="line-block">
<div class="line"><br></div>
</div>
</section>
<section id="table-of-contents" class="">
<span id="id3"></span><h2>Table of contents<a class="headerlink" href="#table-of-contents" title="Permalink to this heading">#</a></h2>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/installation.html">Installation</a><ul>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/installation.html#system-requirements">System requirements</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/installation.html#install-through-pip">Install through pip</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/installation.html#install-through-conda">Install through conda</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/installation.html#install-from-source">Install from source</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/installation.html#check-lifton-installation">Check LiftOn installation</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/installation.html#now-you-are-ready-to-go">Now, you are ready to go !</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/quickstart.html">Quick Start Guide</a><ul>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/quickstart.html#super-quick-start-one-liner">Super-Quick Start (one-liner)</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/quickstart.html#interpreting-outputs-on-the-terminal">Interpreting outputs on the terminal</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/quickstart.html#try-lifton-on-google-colab">Try LiftOn on Google Colab</a></li>
</ul>
</li>
</ul>
</div>
<div class="toctree-wrapper compound">
<p class="caption" role="heading"><span class="caption-text">Examples</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/same_species_liftover/index.html">Same species lift-over</a></li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/close_species_liftover/index.html">Closely related species lift-over</a></li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/distant_species_liftover/index.html">Distantly related species lift-over</a></li>
</ul>
</div>
<div class="toctree-wrapper compound">
<p class="caption" role="heading"><span class="caption-text">Info</span></p>
<ul>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/output_explanation.html">Output files</a><ul>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/output_explanation.html#lifton-gff3">lifton.gff3</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/output_explanation.html#lifton-output">lifton_output/</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/feature_counting.html">Gene / Transcript counting</a><ul>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/feature_counting.html#gene-counting">Gene counting</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/feature_counting.html#transcript-counting">Transcript counting</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/evaluation_metrics.html">Evaluation metrics - sequence identity</a><ul>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/evaluation_metrics.html#dna-sequence-identity-score">DNA sequence identity score</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/evaluation_metrics.html#protein-sequence-identity-score">Protein sequence identity score</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/behind_scenes.html">Behind the scenes</a><ul>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/behind_scenes.html#deciding-chromosomes-and-features-for-annotation-lift-over">Deciding chromosomes and features for annotation lift-over</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/behind_scenes.html#matching-miniprot-liftoff-genome-annotation">Matching miniprot &amp; Liftoff genome annotation</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/behind_scenes.html#protein-maximization-algorithm">Protein-maximization algorithm</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/behind_scenes.html#mutation-report">Mutation report</a></li>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/behind_scenes.html#reference">Reference</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/how_to_page.html">FAQ ...</a></li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/function_manual.html">User Manual</a><ul>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/function_manual.html#lifton">LiftOn</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/changelog.html">Changelog</a><ul>
<li class="toctree-l2"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/changelog.html#v1-0-0">v1.0.0</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/license.html">License</a></li>
<li class="toctree-l1"><a class="reference internal" href="https://ccb.jhu.edu/lifton/content/contact.html">Contact</a></li>
</ul>
</div>
<div class="line-block">
<div class="line"><br></div>
</div>
</section>
<section id="lifton-s-limitation">
<h2>LiftOn's limitation<a class="headerlink" href="#lifton-s-limitation" title="Permalink to this heading">#</a></h2>
<p>LiftOn's <em>chaining algorithm</em> currently only utilizes miniprot alignment results to fix the Liftoff annotation. However, it can be extended to chain together multiple DNA- and protein-based annotation files or aasembled RNA-Seq transcripts.</p>
<p>DNA- and protein-based methods still have some limitations. We are developing a module to merge the LiftOn annotation with the released curated annotations to generate better annotations.</p>
<p>The LiftOn <em>chaining algorithm</em> now does not support multi-threading. This functionality stands as our next targeted feature on the development horizon!</p>
<div class="line-block">
<div class="line"><br></div>
</div>
</section>
</section>

        

## <a name="citation"></a>Citation<a class="headerlink" href="#citation" title="Permalink to this heading">#</a>


Kuan-Hao Chao*, Mihaela Pertea, Steven L Salzberg*, "LiftOn: a tool to improve annotations for protein-coding genes during the lift-over process.", <i>bioRxiv</i> <b>2023.07.27.550754</b>, doi: [https://doi.org/10.1101/2023.07.27.550754](https://doi.org/10.1101/2023.07.27.550754), 2023

<br>
<br>
<br>

<img alt="My Logo" class="logo header-image only-light align-center" src="https://storage.googleapis.com/storage.khchao.com/figures/jhu-logo-dark.png">
