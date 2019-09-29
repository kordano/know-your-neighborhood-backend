(defproject know-your-neighborhood-backend "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.10.0"]
                 [metosin/reitit "0.3.9"]
                 [http-kit "2.3.0"]
                 [metosin/muuntaja "0.6.4"]
                 [clj-time "0.15.1"]
                 [ring-cors "0.1.13"]
                 [org.clojure/data.csv "0.1.4"]
                 [org.clojure/data.json "0.2.6"]
                 [techascent/tech.ml.dataset "1.25"]
                 [mount "0.1.16"]]
  :repl-options {:init-ns know-your-neighborhood-backend.core})
