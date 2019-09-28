(ns know-your-neighborhood-backend.model
  (:require [clojure.spec.alpha :as s]))

(s/def :search/checkAddress string?)
(s/def :search/targetAddress string?)
(s/def :search/service string?)
(s/def :search/servicesToDisplay (s/coll-of :search/service))
(s/def :search/option string?)
(s/def :search/otherOptions (s/coll-of :search/option))

(s/def ::search (s/keys :req-un [:search/checkAddress
                                :search/targetAddress
                                :search/service
                                :search/servicesToDisplay
                                :search/otherOptions]))
