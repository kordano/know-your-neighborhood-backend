(ns know-your-neighborhood-backend.core
  (:gen-class)
  (:require [mount.core :as mount]
            [know-your-neighborhood-backend.server]))

(defn -main [& args]
  (println (mount/start)))

(comment

  (mount/start)

  (mount/stop)

  (-main))
