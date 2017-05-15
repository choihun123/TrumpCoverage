// usage:
//javac -cp stanford-corenlp-full-2016-10-31/*:.  CorefFinder.java
//java -cp stanford-corenlp-full-2016-10-31/*:.  CorefFinder
import java.io.PrintWriter;
import java.util.*;

import java.io.File;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;

import edu.stanford.nlp.coref.CorefCoreAnnotations;
import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

public class CorefFinder {

  public static void main(String[] args) throws Exception {
    String articlesFilename = args[0];
    String outputFilepath = args[1];
    String num = args[2];

    int startNum = Integer.parseInt(num);
    int endNum = startNum + 5;

    File articlesFile = new File(articlesFilename);

    DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
    DocumentBuilder db = dbf.newDocumentBuilder();
    Document document = db.parse(articlesFile);
    NodeList items = document.getDocumentElement().getElementsByTagName("item");

    PrintWriter out = new PrintWriter(outputFilepath);
    Properties props = new Properties();
    props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,mention,coref");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);


    for (int idx = startNum; idx < endNum; idx++) {
      Node n = items.item(idx);

      Node newspaperArticleText = n.getFirstChild();
      String text = newspaperArticleText.getTextContent();

      Annotation doc = new Annotation(text);
      pipeline.annotate(doc);
      Map<Integer, CorefChain> corefs = doc.get(CorefCoreAnnotations.CorefChainAnnotation.class);
      List<CoreMap> sentences = doc.get(CoreAnnotations.SentencesAnnotation.class);

//      int sentenceIdx = 0; // 1 indexed
      for (CoreMap sentence : sentences) {
        List<CoreLabel> tokens = sentence.get(CoreAnnotations.TokensAnnotation.class);
        int tokenIdx = 0;
        for (CoreLabel token : tokens) {

          Integer corefClustId = token.get(CorefCoreAnnotations.CorefClusterIdAnnotation.class);
          CorefChain chain = corefs.get(corefClustId);
          if (chain != null && chain.getMentionsInTextualOrder().size() > 1) {
            CorefChain.CorefMention reprMent = chain.getRepresentativeMention();
            if (reprMent.endIndex - reprMent.startIndex > 10)
                continue;

            out.println("TOKEN INDEX: " + tokenIdx);
//            CorefChain.CorefMention thisMention = (CorefChain.CorefMention) chain.getMentionsWithSameHead(sentenceIdx+1, tokenIdx+1).toArray()[0];
//            out.println("" + thisMention.startIndex + " " + thisMention.endIndex);
            int sentIdx = chain.getRepresentativeMention().sentNum -1;
            CoreMap corefSentence = sentences.get(sentIdx);
            List<CoreLabel> corefSentenceTokens = corefSentence.get(CoreAnnotations.TokensAnnotation.class);
            String resolved = "";
            for (int i = reprMent.startIndex; i < reprMent.endIndex; i++){
                CoreLabel matchedLabel = corefSentenceTokens.get(i-1); //resolved.add(tokens.get(i).word());
                resolved += matchedLabel.word() + " ";
            }
            out.println("FROM: " + token.value());
            out.println("TO: " + resolved);
            out.println("@@@TOKEN@@@");
          }
          tokenIdx += 1;
        }
        out.println("@@@SENTENCE@@@");
//        sentenceIdx += 1;
      }

      out.println("@@@ARTICLE@@@");
    }
    out.close();
  }

}

