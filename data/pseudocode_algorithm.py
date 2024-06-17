for region in regions:
    coordinate_regoin = region.coordinates
    closest_hospitals = find_next_hospital(coordinate_region)


    for hospital in closest_hospitals:
        absolute_population = patient_demand * region.population //1000

        diff_pop = hospital.allgemein_beds.available - hospital.allgemein_beds.used

        if hospital.allgemein_beds.available - hospital.allgemein_beds.used > 0:
            rest_pop =demand = min(hospital.allgemein_beds.available - hospital.allgemein_beds.used,


        if hospital.allgemein_beds.used > 0:
            zuordung.append({region.coordinates, hospital.coordinates, hospital.allgemein_beds.used})