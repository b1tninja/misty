def genwavs():
    ###################### voices #######################
    for voice in voices.values():
        tts.runAndWait()
        tts.setProperty('voice', voice.id)
        tts.runAndWait()

        voice_dir = os.path.join(TTS_BASEDIR, os.path.basename(voice.id))

        # Make directory for TTS output
        if not mkdir(voice_dir):
            continue

        doc_dir = os.path.join(voice_dir, file_name)
        if not mkdir(doc_dir):
            continue

        ################################ GENERATE WAV FILES ################################
        print_and_say(f"{current_speaker()} is reading {file_name}.")

        for i, (section, lines) in enumerate(sections.items(), start=1):
            sec_dir = os.path.join(doc_dir, slugify(section))
            if not mkdir(sec_dir):
                continue

            print_and_say(f"{i}.\t{section}")
            matches = re.finditer(freenode_OnlineCop_re, "\n".join(lines))
            for n, match in enumerate(matches, start=1):
                prefix, title, punctuation, body = match.groups()
                line = match.group(0)
                logging.debug(n, prefix, title)
                wav_out = os.path.join(sec_dir, f'{n}-{slugify(title)}.wav')
                if not os.path.exists(wav_out):
                    tts.save_to_file(line, wav_out)
                    tts.runAndWait()
