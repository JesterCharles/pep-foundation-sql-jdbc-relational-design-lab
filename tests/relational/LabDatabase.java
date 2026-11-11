package relational;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.SecureRandom;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HexFormat;
import java.util.Properties;

/**
 * Creates a new, uniquely named lab database on your local PostgreSQL server, loads schema.sql
 * into it, and drops that database again when the tests finish.
 *
 * Safety: each run invents a fresh name such as relational_design_lab_3f9c0a1b7d2e and creates it.
 * If a database with that name already exists, the run picks another name; it never drops a
 * database it did not create. While the run owns a database, its name is written to
 * target/lab-database.txt, so an interrupted run can be cleaned up by name.
 *
 * Connection: the tests connect over TCP with pgJDBC, using the same environment variables psql reads:
 * PGHOST (a host name or IP address, default localhost), PGPORT (default 5432),
 * PGUSER (default: your login name), PGDATABASE (the existing database used to run
 * CREATE DATABASE and DROP DATABASE, default postgres). The password comes from your password file
 * (PGPASSFILE, or ~/.pgpass, or %APPDATA%\postgresql\pgpass.conf on Windows), which pgJDBC reads
 * like psql does; PGPASSWORD is also accepted.
 */
final class LabDatabase {
    static final String PREFIX = "relational_design_lab_";
    static final Path RECORD = Path.of("target", "lab-database.txt");

    private static final SecureRandom RANDOM = new SecureRandom();
    private static final String DUPLICATE_DATABASE = "42P04";

    /** The database this run created, or null while it owns none. */
    private static String owned;

    private LabDatabase() {
    }

    private static String env(String name, String fallback) {
        String value = System.getenv(name);
        return value == null || value.isBlank() ? fallback : value;
    }

    private static String host() throws SQLException {
        String host = env("PGHOST", "localhost");
        if (host.startsWith("/") || host.contains("\\") || host.contains(",")) {
            throw new SQLException("PGHOST is set to \"" + host + "\", which is not a host name. "
                    + "The tests connect over TCP, so set PGHOST to a host name or IP address such as localhost "
                    + "(see README.md, Setup).");
        }
        return host.contains(":") ? "[" + host + "]" : host;
    }

    private static Connection connect(String database) throws SQLException {
        String url = "jdbc:postgresql://" + host() + ":" + env("PGPORT", "5432") + "/" + database;
        Properties props = new Properties();
        props.setProperty("user", env("PGUSER", System.getProperty("user.name")));
        String password = System.getenv("PGPASSWORD");
        if (password != null && !password.isEmpty()) {
            props.setProperty("password", password);
        }
        // With no password property, pgJDBC looks the password up in the password file.
        return DriverManager.getConnection(url, props);
    }

    private static void admin(String sql) throws SQLException {
        try (Connection c = connect(env("PGDATABASE", "postgres")); Statement s = c.createStatement()) {
            s.execute(sql);
        }
    }

    private static String freshName() {
        byte[] bytes = new byte[6];
        RANDOM.nextBytes(bytes);
        return PREFIX + HexFormat.of().formatHex(bytes);
    }

    /** Creates a new lab database that this run owns and opens a connection to it. */
    static Connection create() throws SQLException, IOException {
        String name = null;
        for (int attempt = 0; attempt < 5 && name == null; attempt++) {
            String candidate = freshName();
            try {
                admin("CREATE DATABASE " + candidate);
                name = candidate;
            } catch (SQLException e) {
                if (DUPLICATE_DATABASE.equals(e.getSQLState())) {
                    continue; // someone else's database has this name: leave it alone and try another
                }
                throw new SQLException("Could not reach PostgreSQL to create the lab database. "
                        + "Check that the server is running and that the connection check in README.md "
                        + "(Prerequisites) works with the same settings. Server said: " + e.getMessage(), e);
            }
        }
        if (name == null) {
            throw new SQLException("Could not find an unused name for the lab database; run the tests again.");
        }
        owned = name;
        Files.createDirectories(RECORD.getParent());
        Files.writeString(RECORD, name + System.lineSeparator());
        return connect(name);
    }

    /** Name of the database this run created, or null. */
    static String ownedName() {
        return owned;
    }

    /** Runs the learner's schema.sql; returns null on success or the error text. */
    static String loadSchema(Connection c) throws IOException {
        String sql = Files.readString(Path.of("schema.sql"));
        try (Statement s = c.createStatement()) {
            s.execute(sql);
            return null;
        } catch (SQLException e) {
            return e.getMessage();
        }
    }

    /** Closes the connection and drops only the database this run created. */
    static void drop(Connection c) throws SQLException, IOException {
        if (c != null) {
            c.close();
        }
        if (owned != null) {
            admin("DROP DATABASE IF EXISTS " + owned);
            owned = null;
            Files.deleteIfExists(RECORD);
        }
    }
}
