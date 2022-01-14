
onClick = () => {
    let state = document.getElementsByName("state")[0]["value"];
    const not_sub_back = document.getElementById("not_sub_back");
    const not_sub = document.getElementById("not_sub");
    const sub = document.getElementById("sub");

    const first_form = document.getElementById("first_form");
    const second_form = document.getElementById("second_form");
    const third_form = document.getElementById("third_form");
    const four_form = document.getElementById("four_form");
    const five_form = document.getElementById("five_form");

    const first = document.getElementById("first");
    const second = document.getElementById("second");
    const third = document.getElementById("third");
    const four = document.getElementById("four");
    const five = document.getElementById("five");
    //constata page 1
    let ktpField = document.getElementById("recruitment1");
    let ktppict = document.getElementById("recruitment2");
    //constanta page 2
    let name = document.getElementById("recruitment5");
    let email = document.getElementById("recruitment6")
    let handphone = document.getElementById("recruitment7");
    let kota_lahir = document.getElementById("state");
    let tgllahir = document.getElementById("birth");
    let gender = document.getElementById("gender_employee");
    let tinggi = document.getElementById("height");
    let berat = document.getElementById("weight");
    let agama = document.getElementById("religion");
    let alamat_ktp = document.getElementById("recruitment8");
    let alamat_domisili = document.getElementById("recruitment9");
    let kota_domisili = document.getElementById("kota_domisili")
    let status_kawin = document.getElementById("status_nikah");
    let nama_socmed = document.getElementById("recruitment10");
    //constanta page 3
    let pendidikan = document.getElementById("employee_education");
    let foto_ijazah = document.getElementById("recruitment11");
    let foto_skck = document.getElementById("recruitment12");
    let foto_profile = document.getElementById("recruitment13");
    let jurusan = document.getElementById("recruitment14");
    let foto_refrensi = document.getElementById("recruitment15");
    //constanta page 4
    let bank_name = document.getElementById("bank_name");
    let nomor_rekening = document.getElementById("recruitment16");
    let foto_tabungan = document.getElementById("recruitment17");
    let name_rekening = document.getElementById("recruitment18");
    let have_npwp = document.getElementById("have_a_npwp");
    let nomor_npwp = document.getElementById("nomor_npwp");
    let foto_npwp = document.getElementById("foto_npwp");
    let foto_bpjtk = document.getElementById("foto_bpjtk");
    let foto_bpjsks = document.getElementById("foto_bpjsks");
    let surat_sehat = document.getElementById("surat_sehat");
    let foto_asuransi = document.getElementById("foto_asuransi");
    let pict_vaksin = document.getElementById("pict_vaksin");
    //constanta page 5
    let first_child_div = document.getElementsByName("first_child_div")[0];
    let pict_first_child_div = document.getElementsByName("pict_first_child_div")[0];
    let second_child_div = document.getElementsByName("second_child_div")[0];
    let pict_second_child_div = document.getElementsByName("pict_second_child_div")[0];
    let third_child_div = document.getElementsByName("third_child_div")[0];
    let pict_third_child_div = document.getElementsByName("pict_third_child_div")[0];



    if (state == 'first') {
        state = document.getElementsByName("state").value;
        let isnum = /^[0][1-15]\d{15}$|^[1-15]\d{15}$/;
        let applicant_ktp = document.getElementsByName("nik_applicant")[0]["value"];

        if (ktpField.value == null | ktpField.value === undefined | ktpField.value == ''|
            ktppict.value == null | ktppict.value === undefined | ktppict.value == '') {
            alert("Pastikan anda mengisi field yang statusnya required");
            state = document.getElementsByName("state")[0]["value"] = "first"

            first_form.classList.remove("d-none");
            second_form.classList.add("d-none");
        }
        else if (ktpField.value && ktppict.value) {
            if (!isnum.test(ktpField.value)) {
                alert("NIK harus 16 digit!.");
                state = document.getElementsByName("state")[0]["value"] = "first"
                first_form.classList.remove("d-none");
                second_form.classList.add("d-none");
            }
            else if (applicant_ktp.includes(ktpField.value)){
                alert("NIK Sudah Terdaftar");
                state = document.getElementsByName("state")[0]["value"] = "first"
                first_form.classList.remove("d-none");
                second_form.classList.add("d-none");
            }
            else if (ktppict.files[0].size > 2097152) {
                alert("Ukuran File/Gambar KTP Max-2Mb!")
                ktppict.value = "";
                state = document.getElementsByName("state")[0]["value"] = "first"
                first_form.classList.remove("d-none");
                second_form.classList.add("d-none");
            }
            else {
                first.classList.add("active");
                second.classList.add("active");

                not_sub_back.classList.remove("d-none");
                not_sub.classList.remove("d-none");
                sub.classList.add("d-none");

                first_form.classList.add("d-none");
                second_form.classList.remove("d-none");
                state = document.getElementsByName("state")[0]["value"] = "second"
            }
        }

        return state
        console.log(state);
    }
    else if (state == 'second') {
        state = document.getElementsByName("state").value;
        let isnum = /^(^62)(\d{3,4}-?){2}\d{3,4}$/;
        let isnum2 = /^\d+$/;
        let emailnum = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;

        if (name.value == null | name.value === undefined | name.value == '' |
            kota_lahir.value == null | kota_lahir.value === undefined | kota_lahir.value == '' |
            tgllahir.value == null | tgllahir.value === undefined | tgllahir.value == '' |
            gender.value == null | gender.value === undefined | gender.value == '' |
            tinggi.value == null | tinggi.value === undefined | tinggi.value == '' |
            berat.value == null | berat.value === undefined | berat.value == '' |
            agama.value == null | agama.value === undefined | agama.value == '' |
            email.value == null | email.value === undefined | email.value == '' |
            handphone.value == null | handphone.value === undefined | handphone.value == '' |
            alamat_ktp.value == null | alamat_ktp.value === undefined | alamat_ktp.value == '' |
            alamat_domisili.value == null | alamat_domisili.value === undefined | alamat_domisili.value == '' |
            kota_domisili.value == null | kota_domisili.value === undefined | kota_domisili.value == '' |
            status_kawin.value == null | status_kawin.value === undefined | status_kawin.value == '' |
            nama_socmed.value == null | nama_socmed.value === undefined | nama_socmed.value == '') {
            alert("Pastikan anda mengisi field yang statusnya required");

            state = document.getElementsByName("state")[0]["value"] = "second"
            second.classList.add("active");
            third.classList.remove("active");

            not_sub_back.classList.remove("d-none");
            not_sub.classList.remove("d-none");
            sub.classList.add("d-none");

            second_form.classList.remove("d-none");
            third_form.classList.add("d-none");

        } else if (email.value && handphone.value) {
            if (!emailnum.test(email.value)) {
                alert("Alamat email tidak valid, mohon cek kembali");
            } else if (!isnum.test(handphone.value)) {
                alert("Mohon isi nomor telepon dengan angka dan format 62.");
            } else {
                first.classList.add("active");
                second.classList.add("active");
                third.classList.add("active");

                not_sub_back.classList.remove("d-none");
                not_sub.classList.remove("d-none");
                sub.classList.add("d-none");

                second_form.classList.add("d-none");
                third_form.classList.remove("d-none");

                state = document.getElementsByName("state")[0]["value"] = "third"
            }
        } else {
            first.classList.add("active");
            second.classList.add("active");
            third.classList.add("active");

            not_sub_back.classList.remove("d-none");
            not_sub.classList.remove("d-none");
            sub.classList.add("d-none");

            second_form.classList.add("d-none");
            third_form.classList.remove("d-none");

            state = document.getElementsByName("state")[0]["value"] = "third"
        }

        return state
        console.log(state);
    }
    else if (state == 'third') {
        state = document.getElementsByName("state").value;

        if (pendidikan.value == null | pendidikan.value === undefined | pendidikan.value == '' |
            foto_ijazah.value == null | foto_ijazah.value === undefined | foto_ijazah.value == '' |
            foto_skck.value == null | foto_skck.value === undefined | foto_skck.value == '' |
            foto_profile.value == null | foto_profile.value === undefined | foto_profile.value == '' |
            jurusan.value == null | jurusan.value === undefined | jurusan.value == '') {
            alert("Pastikan anda mengisi field yang statusnya required");
        }
        else if (foto_ijazah.value && foto_profile.value && foto_profile.value) {
            if (foto_ijazah.files[0].size > 2097152) {
                alert("Ukuran File/Gambar Ijazah Max-2Mb!")
                foto_ijazah.value = "";
            }
            else if (foto_skck.files[0].size > 2097152) {
                alert("Ukuran File/Gambar SKCK Max-2Mb!")
                foto_skck.value = "";
            }
            else if (foto_profile.files[0].size > 2097152) {
                alert("Ukuran File/Gambar Profile Max-2Mb!")
                foto_profile.value = "";
            }
            else if (foto_refrensi.value) {
                if (foto_refrensi.files[0].size > 2097152) {
                    alert("Ukuran File/Gambar Refrensi Max-2Mb!")
                    foto_refrensi.value = "";
                } else {
                    first.classList.add("active");
                    second.classList.add("active");
                    third.classList.add("active");
                    four.classList.add("active");

                    not_sub_back.classList.remove("d-none");
                    not_sub.classList.remove("d-none");
                    sub.classList.add("d-none");

                    third_form.classList.add("d-none");
                    four_form.classList.remove("d-none");

                    state = document.getElementsByName("state")[0]["value"] = "four"

                    console.log(state);
                }
            }
            else {
                first.classList.add("active");
                second.classList.add("active");
                third.classList.add("active");
                four.classList.add("active");

                not_sub_back.classList.remove("d-none");
                not_sub.classList.remove("d-none");
                sub.classList.add("d-none");

                third_form.classList.add("d-none");
                four_form.classList.remove("d-none");

                state = document.getElementsByName("state")[0]["value"] = "four"

                console.log(state);
            }

        }
    }
    else if (state == 'four') {
        state = document.getElementsByName("state").value;
        const digit_bank = $('#bank_name option:selected').attr('digit');
        const digit_bank_value = nomor_rekening.value.length
        let regex_account_number = /^\d+$/;
        if (bank_name.value == null | bank_name.value === undefined | bank_name.value == '' |
            nomor_rekening.value == null | nomor_rekening.value === undefined | nomor_rekening.value == '' |
            foto_tabungan.value == null | foto_tabungan.value === undefined | foto_tabungan.value == '' |
            name_rekening.value == null | name_rekening.value === undefined | name_rekening.value == '') {
            alert("Pastikan anda mengisi field yang statusnya required");
            state = document.getElementsByName("state")[0]["value"] = "four"
            four_form.classList.remove("d-none");
            five_form.classList.add("d-none");
        }
        else if (foto_tabungan.files[0].size > 2097152) {
            alert("Ukuran File/Gambar Tabungan Max-2Mb!")
            foto_tabungan.value = "";
        }
        else if (!regex_account_number.test(nomor_rekening.value)) {
            alert("Nomor Rekening Tidak Valid.");
            nomor_rekening.value = "";
        }
        else if (foto_bpjtk.value && foto_bpjtk.files[0].size > 2097152) {
            alert("Ukuran File/Gambar BPJSTK Max-2Mb!")
            foto_bpjtk.value = "";
        }
        else if (foto_bpjsks.value && foto_bpjsks.files[0].size > 2097152) {
            alert("Ukuran File/Gambar BPJS KS Max-2Mb!")
            foto_bpjsks.value = "";
        }
        else if (surat_sehat.value && surat_sehat.files[0].size > 2097152) {
            alert("Ukuran File/Gambar Surat Sehat Max-2Mb!")
            surat_sehat.value = "";
        }
        else if (pict_vaksin.value && pict_vaksin.files[0].size > 2097152) {
            alert("Ukuran File/Gambar Sertifikat Vaksin Max-2Mb!")
            pict_vaksin.value = "";
        }
        else if (digit_bank != digit_bank_value ) {
            alert("Digit Bank tidak sesuai dengan pilihan Bank!")
            nomor_rekening.value = "";
        }
        else if(have_npwp.checked){
            if (nomor_npwp.value == null | nomor_npwp.value === undefined | nomor_npwp.value == '' |
                foto_npwp.value == null | foto_npwp.value === undefined | foto_npwp.value == ''){
                alert("Pastikan anda mengisi field yang statusnya required");
            }
            else if(foto_npwp.files[0].size > 2097152){
                alert("Ukuran File/Gambar NPWP Max-2Mb!")
                foto_npwp.value = "";
            }
            else {
                if(status_kawin.value == 'k1'| status_kawin.value == 'tk1') {
                    first_child_div.classList.remove("d-none");
                    pict_first_child_div.classList.remove("d-none")
                }
                else if(status_kawin.value == 'k2'| status_kawin.value == 'tk2') {
                    first_child_div.classList.remove("d-none");
                    pict_first_child_div.classList.remove("d-none")
                    second_child_div.classList.remove("d-none");
                    pict_second_child_div.classList.remove("d-none")
                }
                else if(status_kawin.value == 'k3'| status_kawin.value == 'tk3') {
                    first_child_div.classList.remove("d-none");
                    pict_first_child_div.classList.remove("d-none")
                    second_child_div.classList.remove("d-none");
                    pict_second_child_div.classList.remove("d-none")
                    third_child_div.classList.remove("d-none");
                    pict_third_child_div.classList.remove("d-none")
                }
                first.classList.add("active");
                second.classList.add("active");
                third.classList.add("active");
                four.classList.add("active");
                five.classList.add("active");

                not_sub_back.classList.remove("d-none");
                not_sub.classList.add("d-none");
                sub.classList.remove("d-none");

                four_form.classList.add("d-none");
                five_form.classList.remove("d-none");

                state = document.getElementsByName("state")[0]["value"] = "five"
                console.log(state);
            }
        }
        else{
            if(status_kawin.value == 'k1'| status_kawin.value == 'tk1') {
                first_child_div.classList.remove("d-none");
                pict_first_child_div.classList.remove("d-none")
            }
            else if(status_kawin.value == 'k2'| status_kawin.value == 'tk2') {
                first_child_div.classList.remove("d-none");
                pict_first_child_div.classList.remove("d-none")
                second_child_div.classList.remove("d-none");
                pict_second_child_div.classList.remove("d-none")
            }
            else if(status_kawin.value == 'k3'| status_kawin.value == 'tk3') {
                first_child_div.classList.remove("d-none");
                pict_first_child_div.classList.remove("d-none")
                second_child_div.classList.remove("d-none");
                pict_second_child_div.classList.remove("d-none")
                third_child_div.classList.remove("d-none");
                pict_third_child_div.classList.remove("d-none")
            }
            first.classList.add("active");
            second.classList.add("active");
            third.classList.add("active");
            four.classList.add("active");
            five.classList.add("active");

            not_sub_back.classList.remove("d-none");
            not_sub.classList.add("d-none");
            sub.classList.remove("d-none");

            four_form.classList.add("d-none");
            five_form.classList.remove("d-none");

            state = document.getElementsByName("state")[0]["value"] = "five"
            console.log(state);
        }
    }

}

onClickSubmit = () => {
    let pict_kk = document.getElementsByName("foto_kk")[0];
    if (pict_kk.value) {
        if(pict_kk.files[0].size > 2097152){
            alert("Ukuran File/Gambar Max-2Mb!")
            pict_kk.value = "";
        }

    }

}

onClickBack = () => {
    let state = document.getElementsByName("state")[0]['value'];
    const not_sub_back = document.getElementById("not_sub_back");
    const not_sub = document.getElementById("not_sub");
    const sub = document.getElementById("sub");

    const first_form = document.getElementById("first_form");
    const second_form = document.getElementById("second_form");
    const third_form = document.getElementById("third_form");
    const four_form = document.getElementById("four_form");
    const five_form = document.getElementById("five_form");
    const six_form = document.getElementById("six_form");

    const first = document.getElementById("first");
    const second = document.getElementById("second");
    const third = document.getElementById("third");
    const four = document.getElementById("four");
    const five = document.getElementById("five");

    if(state == 'second') {

        first.classList.add("active");
        second.classList.remove("active");

        not_sub_back.classList.add("d-none");
        not_sub.classList.remove("d-none");
        sub.classList.add("d-none");

        first_form.classList.remove("d-none");
        second_form.classList.add("d-none");

        state = document.getElementsByName("state")[0]["value"]="first"

        console.log(state);
    }
    else if (state == 'third') {

        second.classList.add("active");
        third.classList.remove("active");

        not_sub_back.classList.remove("d-none");
        not_sub.classList.remove("d-none");
        sub.classList.add("d-none");

        second_form.classList.remove("d-none");
        third_form.classList.add("d-none");

        state = document.getElementsByName("state")[0]["value"]="second"

        console.log(state);
    }
    else if (state == 'four') {

        third.classList.add("active");
        four.classList.remove("active");

        not_sub_back.classList.remove("d-none");
        not_sub.classList.remove("d-none");
        sub.classList.add("d-none");

        third_form.classList.remove("d-none");
        four_form.classList.add("d-none");

        state = document.getElementsByName("state")[0]["value"]="third"

        console.log(state);
    }
    else if (state == 'five') {

        four.classList.add("active");
        five.classList.remove("active");

        not_sub_back.classList.remove("d-none");
        not_sub.classList.remove("d-none");
        sub.classList.add("d-none");

        four_form.classList.remove("d-none");
        five_form.classList.add("d-none");

        state = document.getElementsByName("state")[0]["value"]="four"

        console.log(state);
    }
}

toggleNPWP = (e) => {
    let npwp_div = document.getElementsByName("npwp_div")[0];
    let pict_npwp_div = document.getElementsByName("pict_npwp_div")[0];
    if (e.checked) {
        npwp_div.classList.remove("d-none");
        pict_npwp_div.classList.remove("d-none");
    } else {
        npwp_div.classList.add("d-none");
        pict_npwp_div.classList.add("d-none");
    }
}