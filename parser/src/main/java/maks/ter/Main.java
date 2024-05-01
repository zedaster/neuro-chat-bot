package maks.ter;

import java.io.File;
import java.io.Serial;
import java.util.HashMap;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

public class Main {
    public static void main(String[] args) {
        Document doc;
        try {
            //doc = Jsoup.connect("https://urfu.ru/ru/feedback/priem/obshchie-voprosy-po-priemu").get();
            doc = Jsoup.parse(new File("/example_html.html"));
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }

        HashMap<String, String> questionAnswer = new HashMap<>();
        String prevQuestion = null;

        for (Element element: doc.body().getElementsByClass("urfu-feedback")) {

            for (Element div: element.children()) {
                System.out.println(prevQuestion);

                if (prevQuestion == null && div.className().equals("question")) {
                    prevQuestion = div.text();
                    continue;
                }

                if (prevQuestion != null && div.className().equals("answer")) {
                    questionAnswer.put(prevQuestion, div.text());
                    prevQuestion = null;
                }
            }
        }

        questionAnswer.entrySet().forEach(data ->
            System.out.println(data.getKey() + ">>>>>>>>>>>>>: " + data.getValue())
        );
    }
}