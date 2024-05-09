package maks.ter;

import lombok.val;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.boot.Metadata;
import org.hibernate.boot.MetadataSources;
import org.hibernate.boot.registry.StandardServiceRegistry;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.rmi.server.UID;
import java.util.AbstractQueue;
import java.util.HashMap;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

// 16, 27
public class MainWriteHtml {

    public static void main(String[] args) throws IOException, InterruptedException {

        SessionFactory sessionFactory = DatabaseService.createSession();

        ExecutorService service = Executors.newFixedThreadPool(30);


        for (int i = 2; i <= 51; i++) {

            System.out.println("Iteration number: " + i);
            AtomicInteger page = new AtomicInteger(i * 30);
            final int max = 30 * (i + 1);

            while (page.intValue() < max) {
                service.submit(() -> {
                    try {
                        writeHtml(page.incrementAndGet(), max, sessionFactory.openSession());
                    } catch (IOException e) {
                        System.out.println(e);
                    }
                });
            }

            System.out.println("Thread sleep");
            Thread.sleep(180000L);
        }

        service.shutdown();
    }

    private static void writeHtml(Integer page, Integer max, Session session) throws IOException {

        if (page > max) {
            return;
        }

        System.out.println("Try get html from page: " + "https://urfu.ru/ru/feedback/priem/obshchie-voprosy-po-priemu?tx_urfu_question[@widget_0][currentPage]="+page);

        Document doc = Jsoup.parse(new URL("https://urfu.ru/ru/feedback/priem/obshchie-voprosy-po-priemu?tx_urfu_question[action]=index&tx_urfu_question[controller]=Feedback&tx_urfu_question[@widget_0][currentPage]="+page), 30000000);

        HashMap<String, String> questionAnswers = new HashMap<>();
        String prevQuestion = null;

        for (Element element: doc.body().getElementsByClass("urfu-feedback")) {

            for (Element div: element.children()) {

                if (div.className().equals("question")) {
                    prevQuestion = div.text();
                    continue;
                }

                if (prevQuestion != null) {
                    if (div.className().equals("answer")) {
                        questionAnswers.put(prevQuestion, div.text());
                    }
                    prevQuestion = null;
                }
            }
        }

        System.out.println("Get html from page: " + page + "\t\tCount entities: " + questionAnswers.size());

        session.beginTransaction();

        for (var entity: questionAnswers.entrySet()) {
            QuestionAnswer questionAnswer = new QuestionAnswer();
            questionAnswer.setUuid(UUID.randomUUID().toString());
            questionAnswer.setQuestion(entity.getKey());
            questionAnswer.setAnswer(entity.getValue());

            session.save(questionAnswer);
        }

        session.getTransaction().commit();
        session.close();
    }
}
