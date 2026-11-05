from datetime import timedelta

def calculate_amount(room,no_of_guests,check_in,check_out,breakfast,stays):
    nights=(check_out-check_in).days
    room_amount=0
    guest_amount=0
    breakfast_amount=0
    nights_details=[]

    current_date=check_in
    while current_date<check_out:
        tariff=room.get_tariff()
        if current_date.weekday()==4 or current_date.weekday()==5:
            tariff=tariff+(tariff*20/100)
        extra_guest=room.guest_charges(no_of_guests)
        breakfast_charge=room.cost_breakfast(no_of_guests,breakfast)
        room_amount+=tariff
        guest_amount+=extra_guest
        breakfast_amount+=breakfast_charge
        nights_details.append({
            "date":current_date,
            "room_tariff":tariff,
            "extra_guest":extra_guest,
            "breakfast":breakfast_charge
        })
        current_date=current_date+timedelta(days=1)
    room_charges=room_amount
    stay_discount=0
    if nights>=7:
        stay_discount=room_charges*10/100
    loyalty_discount=0
    if stays>=3:
        loyalty_discount=(room_charges-stay_discount+guest_amount+breakfast_amount)*5/100
    total_before_gst=(room_charges+guest_amount+breakfast_amount-stay_discount-loyalty_discount)
    gst_amount=0
    for row in nights_details:
        night_total=(row["room_tariff"]+row["extra_guest"]+row["breakfast"])
        if(room_amount+guest_amount+breakfast_amount)>0:
            discount=(stay_discount+loyalty_discount)*night_total/(room_amount+guest_amount+breakfast_amount)
        else:
            discount=0
        remain_amount=night_total-discount
        if row["room_tariff"]>7500:
            gst=remain_amount*18/100
        else:
            gst=remain_amount*12/100
        gst_amount+=gst
    total_amount=total_before_gst+gst_amount
    return {
        "nights": nights,
        "room_amount": room_amount,
        "guest_amount": guest_amount,
        "breakfast_amount": breakfast_amount,
        "stay_discount": stay_discount,
        "loyalty_discount": loyalty_discount,
        "gst_amount": gst_amount,
        "total_amount": total_amount,
        "night_details": nights_details
    }
    