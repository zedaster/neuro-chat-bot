package maks.ter;

import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;

public class DatabaseService {

    public static SessionFactory createSession() {
        Configuration configuration = new Configuration().configure();
        configuration.addAnnotatedClass(QuestionAnswer.class);

        StandardServiceRegistryBuilder builder = new StandardServiceRegistryBuilder().applySettings(configuration.getProperties());
        return configuration.buildSessionFactory(builder.build());
    }
}
