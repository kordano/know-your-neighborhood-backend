(ns know-your-neighborhood-backend.data
  (:require [tech.ml.dataset :as dataset]
            [clojure.java.jdbc :as j]
            [clojure.data.csv :as csv]
            [clojure.java.io :as io]
            [clojure.java.jdbc :as jdbc]))


(def raw-data
  (-> "resources/data.csv"
      dataset/->dataset
      (dataset/->flyweight :error-on-missing-values? false)
      ))


(first raw-data)


(def data (->> raw-data
               (map #(select-keys % ["Selite_en" "Longitude" "Latitude" "N_GK25" "E_GK25" "Name_fi" "Name_en"]))
               ))



(def selected-services {"health" ["Dental Care" "School and student health services" "Doctor's reception" "Health stations" ]
                        "safety" ["Police departments and stations"]
                        "daycare" ["Pre-primary education organised by day care" "Supervised playground activities" "pre-primary education" "day care"]
                        "education" ["Polytechnic education in Finnish" "Upper secondary school education, general programme" "education in English" "education in Finnish" "education in Swedish"]
                        "traffic" ["Public libraries" "Terminals" "Water bus platforms" ]
                        "culture" ["Cinemas" "Art museums" "Cultural history museums" "Green areas" ]
                        })

(def reverse-selected
  (into {} (mapcat (fn [[k vs]] (map (fn [v] [v k]) vs)) selected-services)))

(def selected-fields (into #{} (mapcat val selected-services)))

(def selected-data (->> data
                        (filter #(contains? selected-fields (get % "Selite_en")))
                        (map #(update-in % ["Selite_en"] reverse-selected))))


(with-open [writer (io/writer "dump.csv")]
  (csv/write-csv writer
                 (let [selected-keys (-> selected-data first keys vec)]
                   (->> selected-data
                        (mapv (fn [d] (mapv d selected-keys)))
                        (into [selected-keys])))))
