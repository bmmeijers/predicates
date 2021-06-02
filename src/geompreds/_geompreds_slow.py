SPLITTER = 134217729
EPSILON = 0.000000000000000111022302462515654042363166809082031250000000000000
RESULTERRBOUND = (3.0 + 8.0 * EPSILON) * EPSILON
CCWERRBOUND_A = (3.0 + 16.0 * EPSILON) * EPSILON
CCWERRBOUND_B = (2.0 + 12.0 * EPSILON) * EPSILON
CCWERRBOUND_C = (9.0 + 64.0 * EPSILON) * EPSILON * EPSILON
ICCERRBOUND_A = (10.0 + 96.0 * EPSILON) * EPSILON
ICCERRBOUND_B = (4.0 + 48.0 * EPSILON) * EPSILON
ICCERRBOUND_C = (44.0 + 576.0 * EPSILON) * EPSILON * EPSILON


def orient2d(pa, pb, pc):
    detleft = (pa[0] - pc[0]) * (pb[1] - pc[1])
    detright = (pa[1] - pc[1]) * (pb[0] - pc[0])
    det = detleft - detright
    if detleft > 0.0:
        if detright <= 0.0:
            return det
        else:
            detsum = detleft + detright
    elif detleft < 0.0:
        if detright >= 0.0:
            return det
        else:
            detsum = -detleft - detright
    else:
        return det
    errbound = CCWERRBOUND_A * detsum
    if det >= errbound or -det >= errbound:
        return det
    else:
        return orient2dadapt(pa, pb, pc, detsum)


def orient2dadapt(pa, pb, pc, detsum):
    acx = pa[0] - pc[0]
    bcx = pb[0] - pc[0]
    acy = pa[1] - pc[1]
    bcy = pb[1] - pc[1]

    (detleft, detlefttail) = two_product(acx, bcy)
    (detright, detrighttail) = two_product(acy, bcx)

    (B3, B2, B1, B0) = two_two_diff(detleft, detlefttail, detright, detrighttail)
    B = [B0, B1, B2, B3]

    det = estimate(B)
    errbound = CCWERRBOUND_B * detsum
    if det >= errbound or (-det >= errbound):
        return det

    acxtail = two_diff_tail(pa[0], pc[0], acx)
    bcxtail = two_diff_tail(pb[0], pc[0], bcx)
    acytail = two_diff_tail(pa[1], pc[1], acy)
    bcytail = two_diff_tail(pb[1], pc[1], bcy)

    if acxtail == 0.0 and acytail == 0.0 and bcxtail == 0.0 and bcytail == 0.0:
        return det

    errbound = CCWERRBOUND_C * detsum + RESULTERRBOUND * abs(det)
    det += (acx * bcytail + bcy * acxtail) - (acy * bcxtail + bcx * acytail)

    if det >= errbound or -det >= errbound:
        return det

    (s1, s0) = two_product(acxtail, bcy)
    (t1, t0) = two_product(acytail, bcx)
    (u3, u2, u1, u0) = two_two_diff(s1, s0, t1, t0)
    U = [u0, u1, u2, u3]

    C1 = [0.0] * 8
    c1length = fast_expansion_sum_zeroelim(B, U, C1)

    (s1, s0) = two_product(acx, bcytail)
    (t1, t0) = two_product(acy, bcxtail)
    (u3, u2, u1, u0) = two_two_diff(s1, s0, t1, t0)
    U = [u0, u1, u2, u3]

    C2 = [0.0] * 12
    c2length = fast_expansion_sum_zeroelim(C1[:c1length], U, C2)

    (s1, s0) = two_product(acxtail, bcytail)
    (t1, t0) = two_product(acytail, bcxtail)
    (u3, u2, u1, u0) = two_two_diff(s1, s0, t1, t0)
    U = [u0, u1, u2, u3]
    D = [0.0] * 16
    dlength = fast_expansion_sum_zeroelim(C2[:c2length], U, D)
    return D[dlength - 1]


def incircle(pa, pb, pc, pd):
    adx = pa[0] - pd[0]
    bdx = pb[0] - pd[0]
    cdx = pc[0] - pd[0]
    ady = pa[1] - pd[1]
    bdy = pb[1] - pd[1]
    cdy = pc[1] - pd[1]

    bdxcdy = bdx * cdy
    cdxbdy = cdx * bdy
    alift = adx * adx + ady * ady

    cdxady = cdx * ady
    adxcdy = adx * cdy
    blift = bdx * bdx + bdy * bdy

    adxbdy = adx * bdy
    bdxady = bdx * ady
    clift = cdx * cdx + cdy * cdy

    det = (
        alift * (bdxcdy - cdxbdy)
        + blift * (cdxady - adxcdy)
        + clift * (adxbdy - bdxady)
    )

    permanent = (
        (abs(bdxcdy) + abs(cdxbdy)) * alift
        + (abs(cdxady) + abs(adxcdy)) * blift
        + (abs(adxbdy) + abs(bdxady)) * clift
    )
    errbound = ICCERRBOUND_A * permanent
    if det > errbound or -det > errbound:
        return det
    return incircleadapt(pa, pb, pc, pd, permanent)


def incircleadapt(pa, pb, pc, pd, permanent):
    temp8 = [0.0] * 8
    temp16a = [0.0] * 16
    temp16b = [0.0] * 16
    temp16c = [0.0] * 16
    temp32a = [0.0] * 32
    temp32b = [0.0] * 32
    temp48 = [0.0] * 48
    temp64 = [0.0] * 64

    adx = pa[0] - pd[0]
    bdx = pb[0] - pd[0]
    cdx = pc[0] - pd[0]
    ady = pa[1] - pd[1]
    bdy = pb[1] - pd[1]
    cdy = pc[1] - pd[1]

    (bdxcdy1, bdxcdy0) = two_product(bdx, cdy)
    (cdxbdy1, cdxbdy0) = two_product(cdx, bdy)
    (bc3, bc2, bc1, bc0) = two_two_diff(bdxcdy1, bdxcdy0, cdxbdy1, cdxbdy0)
    bc = [bc0, bc1, bc2, bc3]

    axbc = [0.0] * 8
    axbclen = scale_expansion_zeroelim(bc, adx, axbc)
    axxbc = [0.0] * 16
    axxbclen = scale_expansion_zeroelim(axbc[:axbclen], adx, axxbc)
    aybc = [0.0] * 8
    aybclen = scale_expansion_zeroelim(bc, ady, aybc)
    ayybc = [0.0] * 16
    ayybclen = scale_expansion_zeroelim(aybc[:aybclen], ady, ayybc)
    adet = [0.0] * 32
    alen = fast_expansion_sum_zeroelim(axxbc[0:axxbclen], ayybc[0:ayybclen], adet)

    (cdxady1, cdxady0) = two_product(cdx, ady)
    (adxcdy1, adxcdy0) = two_product(adx, cdy)
    (c3, c2, c1, c0) = two_two_diff(cdxady1, cdxady0, adxcdy1, adxcdy0)
    ca = [c0, c1, c2, c3]

    bxca = [0.0] * 8
    bxcalen = scale_expansion_zeroelim(ca, bdx, bxca)
    bxxca = [0.0] * 16
    bxxcalen = scale_expansion_zeroelim(bxca[:bxcalen], bdx, bxxca)
    byca = [0.0] * 8
    bycalen = scale_expansion_zeroelim(ca, bdy, byca)
    byyca = [0.0] * 16
    byycalen = scale_expansion_zeroelim(byca[:bycalen], bdy, byyca)
    bdet = [0.0] * 32
    blen = fast_expansion_sum_zeroelim(bxxca[:bxxcalen], byyca[0:byycalen], bdet)

    (adxbdy1, adxbdy0) = two_product(adx, bdy)
    (bdxady1, bdxady0) = two_product(bdx, ady)
    (ab3, ab2, ab1, ab0) = two_two_diff(adxbdy1, adxbdy0, bdxady1, bdxady0)
    ab = [ab0, ab1, ab2, ab3]

    cxab = [0.0] * 8
    cxablen = scale_expansion_zeroelim(ab, cdx, cxab)
    cxxab = [0.0] * 16
    cxxablen = scale_expansion_zeroelim(cxab[:cxablen], cdx, cxxab)
    cyab = [0.0] * 8
    cyablen = scale_expansion_zeroelim(ab, cdy, cyab)
    cyyab = [0.0] * 16
    cyyablen = scale_expansion_zeroelim(cyab[:cyablen], cdy, cyyab)
    cdet = [0.0] * 32
    clen = fast_expansion_sum_zeroelim(cxxab[:cxxablen], cyyab[:cyyablen], cdet)

    abdet = [0.0] * 64
    ablen = fast_expansion_sum_zeroelim(adet[:alen], bdet[:blen], abdet)
    fin1 = [0.0] * 1152
    finlength = fast_expansion_sum_zeroelim(abdet[:ablen], cdet[:clen], fin1)

    det = estimate(fin1[:finlength])
    errbound = ICCERRBOUND_B * permanent
    if det >= errbound or -det >= errbound:
        return det

    adxtail = two_diff_tail(pa[0], pd[0], adx)
    adytail = two_diff_tail(pa[1], pd[1], ady)
    bdxtail = two_diff_tail(pb[0], pd[0], bdx)
    bdytail = two_diff_tail(pb[1], pd[1], bdy)
    cdxtail = two_diff_tail(pc[0], pd[0], cdx)
    cdytail = two_diff_tail(pc[1], pd[1], cdy)

    if (
        adxtail == 0.0
        and bdxtail == 0.0
        and cdxtail == 0.0
        and adytail == 0.0
        and bdytail == 0.0
        and cdytail == 0.0
    ):
        return det

    errbound = ICCERRBOUND_C * permanent + RESULTERRBOUND * abs(det)
    det += (
        (
            (adx * adx + ady * ady)
            * ((bdx * cdytail + cdy * bdxtail) - (bdy * cdxtail + cdx * bdytail))
            + 2.0 * (adx * adxtail + ady * adytail) * (bdx * cdy - bdy * cdx)
        )
        + (
            (bdx * bdx + bdy * bdy)
            * ((cdx * adytail + ady * cdxtail) - (cdy * adxtail + adx * cdytail))
            + 2.0 * (bdx * bdxtail + bdy * bdytail) * (cdx * ady - cdy * adx)
        )
        + (
            (cdx * cdx + cdy * cdy)
            * ((adx * bdytail + bdy * adxtail) - (ady * bdxtail + bdx * adytail))
            + 2.0 * (cdx * cdxtail + cdy * cdytail) * (adx * bdy - ady * bdx)
        )
    )
    if det >= errbound or -det >= errbound:
        return det

    fin2 = [0.0] * 1152

    aa = [0.0] * 4
    if bdxtail != 0.0 or bdytail != 0.0 or cdxtail != 0.0 or cdytail != 0.0:
        (adxadx1, adxadx0) = square(adx)
        (adyady1, adyady0) = square(ady)
        (aa3, aa2, aa1, aa0) = two_two_sum(adxadx1, adxadx0, adyady1, adyady0)
        aa = [aa0, aa1, aa2, aa3]

    bb = [0.0] * 4
    if cdxtail != 0.0 or cdytail != 0.0 or adxtail != 0.0 or adytail != 0.0:
        (bdxbdx1, bdxbdx0) = square(bdx)
        (bdybdy1, bdybdy0) = square(bdy)
        (bb3, bb2, bb1, bb0) = two_two_sum(bdxbdx1, bdxbdx0, bdybdy1, bdybdy0)
        bb = [bb0, bb1, bb2, bb3]

    cc = [0.0] * 4
    if adxtail != 0.0 or adytail != 0.0 or bdxtail != 0.0 or bdytail != 0.0:
        (cdxcdx1, cdxcdx0) = square(cdx)
        (cdycdy1, cdycdy0) = square(cdy)
        (cc3, cc2, cc1, cc0) = two_two_sum(cdxcdx1, cdxcdx0, cdycdy1, cdycdy0)
        cc = [cc0, cc1, cc2, cc3]

    axtbclen = 9
    axtbc = [0.0] * 8
    if adxtail != 0.0:
        axtbclen = scale_expansion_zeroelim(bc, adxtail, axtbc)
        temp16a = [0.0] * 16
        temp16alen = scale_expansion_zeroelim(axtbc[:axtbclen], 2.0 * adx, temp16a)

        axtcc = [0.0] * 8
        axtcclen = scale_expansion_zeroelim(cc, adxtail, axtcc)
        temp16b = [0.0] * 16
        temp16blen = scale_expansion_zeroelim(axtcc[:axtcclen], bdy, temp16b)

        axtbb = [0.0] * 8
        axtbblen = scale_expansion_zeroelim(bb, adxtail, axtbb)
        temp16c = [0.0] * 16
        temp16clen = scale_expansion_zeroelim(axtbb[:axtbblen], -cdy, temp16c)

        temp32a = [0.0] * 32
        temp32alen = fast_expansion_sum_zeroelim(
            temp16a[:temp16alen], temp16b[:temp16blen], temp32a
        )
        temp48 = [0.0] * 48
        temp48len = fast_expansion_sum_zeroelim(
            temp16c[:temp16clen], temp32a[:temp32alen], temp48
        )
        finlength = fast_expansion_sum_zeroelim(
            fin1[:finlength], temp48[:temp48len], fin2
        )
        fin2, fin1 = fin1, fin2

    aytbclen = 9
    aytbc = [0.0] * 8
    if adytail != 0.0:
        aytbclen = scale_expansion_zeroelim(bc, adytail, aytbc)
        temp16alen = scale_expansion_zeroelim(aytbc[:aytbclen], 2.0 * ady, temp16a)
        aytbb = [0.0] * 8
        aytbblen = scale_expansion_zeroelim(bb, adytail, aytbb)
        temp16blen = scale_expansion_zeroelim(aytbb[:aytbblen], cdx, temp16b)

        aytcc = [0.0] * 8
        aytcclen = scale_expansion_zeroelim(cc, adytail, aytcc)
        temp16clen = scale_expansion_zeroelim(aytcc[:aytcclen], -bdx, temp16c)

        temp32alen = fast_expansion_sum_zeroelim(
            temp16a[:temp16alen], temp16b[:temp16blen], temp32a
        )

        temp48len = fast_expansion_sum_zeroelim(
            temp16c[:temp16clen], temp32a[:temp32alen], temp48
        )
        finlength = fast_expansion_sum_zeroelim(
            fin1[:finlength], temp48[:temp48len], fin2
        )
        fin2, fin1 = fin1, fin2

    bxtcalen = 9
    bxtca = [0.0] * 8
    if bdxtail != 0.0:
        bxtcalen = scale_expansion_zeroelim(ca, bdxtail, bxtca)
        temp16alen = scale_expansion_zeroelim(bxtca[:bxtcalen], 2.0 * bdx, temp16a)

        bxtaa = [0.0] * 8
        bxtaalen = scale_expansion_zeroelim(aa, bdxtail, bxtaa)
        temp16blen = scale_expansion_zeroelim(bxtaa[:bxtaalen], cdy, temp16b)

        bxtcc = [0.0] * 8
        bxtcclen = scale_expansion_zeroelim(cc, bdxtail, bxtcc)
        temp16clen = scale_expansion_zeroelim(bxtcc[:bxtcclen], -ady, temp16c)

        temp32alen = fast_expansion_sum_zeroelim(
            temp16a[:temp16alen], temp16b[:temp16blen], temp32a
        )
        temp48len = fast_expansion_sum_zeroelim(
            temp16c[:temp16clen], temp32a[:temp32alen], temp48
        )
        finlength = fast_expansion_sum_zeroelim(
            fin1[:finlength], temp48[:temp48len], fin2
        )
        fin2, fin1 = fin1, fin2

    bytcalen = 9
    bytca = [0.0] * 8
    if bdytail != 0.0:
        bytcalen = scale_expansion_zeroelim(ca, bdytail, bytca)
        temp16alen = scale_expansion_zeroelim(bytca[:bytcalen], 2.0 * bdy, temp16a)

        bytcc = [0.0] * 8
        bytcclen = scale_expansion_zeroelim(cc, bdytail, bytcc)
        temp16blen = scale_expansion_zeroelim(bytcc[:bytcclen], adx, temp16b)

        bytaa = [0.0] * 8
        bytaalen = scale_expansion_zeroelim(aa, bdytail, bytaa)
        temp16clen = scale_expansion_zeroelim(bytaa[:bytaalen], -cdx, temp16c)

        temp32alen = fast_expansion_sum_zeroelim(
            temp16a[:temp16alen], temp16b[:temp16blen], temp32a
        )
        temp48len = fast_expansion_sum_zeroelim(
            temp16c[:temp16clen], temp32a[:temp32alen], temp48
        )

        finlength = fast_expansion_sum_zeroelim(
            fin1[:finlength], temp48[:temp48len], fin2
        )
        fin2, fin1 = fin1, fin2

    cxtab = [0.0] * 8
    cxtablen = 9
    if cdxtail != 0.0:
        cxtablen = scale_expansion_zeroelim(ab, cdxtail, cxtab)
        temp16alen = scale_expansion_zeroelim(cxtab[:cxtablen], 2.0 * cdx, temp16a)

        cxtbb = [0.0] * 8
        cxtbblen = scale_expansion_zeroelim(bb, cdxtail, cxtbb)
        temp16blen = scale_expansion_zeroelim(cxtbb[:cxtbblen], ady, temp16b)

        cxtaa = [0.0] * 8
        cxtaalen = scale_expansion_zeroelim(aa, cdxtail, cxtaa)
        temp16clen = scale_expansion_zeroelim(cxtaa[:cxtaalen], -bdy, temp16c)

        temp32alen = fast_expansion_sum_zeroelim(
            temp16a[:temp16alen], temp16b[:temp16blen], temp32a
        )
        temp48len = fast_expansion_sum_zeroelim(
            temp16c[:temp16clen], temp32a[:temp32alen], temp48
        )
        finlength = fast_expansion_sum_zeroelim(
            fin1[:finlength], temp48[:temp48len], fin2
        )
        fin2, fin1 = fin1, fin2

    cytab = [0.0] * 8
    cytablen = 9
    if cdytail != 0.0:
        cytablen = scale_expansion_zeroelim(ab, cdytail, cytab)
        temp16alen = scale_expansion_zeroelim(cytab[:cytablen], 2.0 * cdy, temp16a)

        cytaa = [0.0] * 8
        cytaalen = scale_expansion_zeroelim(aa, cdytail, cytaa)
        temp16blen = scale_expansion_zeroelim(cytaa[:cytaalen], bdx, temp16b)

        cytbb = [0.0] * 8
        cytbblen = scale_expansion_zeroelim(bb, cdytail, cytbb)
        temp16clen = scale_expansion_zeroelim(cytbb[:cytbblen], -adx, temp16c)

        temp32alen = fast_expansion_sum_zeroelim(
            temp16a[:temp16alen], temp16b[:temp16blen], temp32a
        )
        temp48len = fast_expansion_sum_zeroelim(
            temp16c[:temp16clen], temp32a[:temp32alen], temp48
        )
        finlength = fast_expansion_sum_zeroelim(
            fin1[:finlength], temp48[:temp48len], fin2
        )
        fin2, fin1 = fin1, fin2

    if adxtail != 0.0 or adytail != 0.0:
        bctt = [0.0] * 4
        bct = [0.0] * 8
        if bdxtail != 0.0 or bdytail != 0.0 or cdxtail != 0.0 or cdytail != 0.0:
            (ti1, ti0) = two_product(bdxtail, cdy)
            (tj1, tj0) = two_product(bdx, cdytail)
            (u3, u2, u1, u0) = two_two_sum(ti1, ti0, tj1, tj0)
            u = [u0, u1, u2, u3]
            negate = -bdy
            (ti1, ti0) = two_product(cdxtail, negate)
            negate = -bdytail
            (tj1, tj0) = two_product(cdx, negate)
            (v3, v2, v1, v0) = two_two_sum(ti1, ti0, tj1, tj0)
            v = [v0, v1, v2, v3]
            bctlen = fast_expansion_sum_zeroelim(u, v, bct)
            (ti1, ti0) = two_product(bdxtail, cdytail)
            (tj1, tj0) = two_product(cdxtail, bdytail)
            (bctt3, bctt2, bctt1, bctt0) = two_two_diff(ti1, ti0, tj1, tj0)
            bctt = [bctt0, bctt1, bctt2, bctt3]
            bcttlen = 4
        else:
            bct[0] = 0.0
            bctlen = 1
            bctt[0] = 0.0
            bcttlen = 1

        if adxtail != 0.0:
            temp16alen = scale_expansion_zeroelim(axtbc[:axtbclen], adxtail, temp16a)
            axtbct = [0.0] * 16
            axtbctlen = scale_expansion_zeroelim(bct[:bctlen], adxtail, axtbct)
            temp32alen = scale_expansion_zeroelim(
                axtbct[:axtbctlen], 2.0 * adx, temp32a
            )
            temp48len = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp32a[:temp32alen], temp48
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp48[:temp48len], fin2
            )
            fin2, fin1 = fin1, fin2

            if bdytail != 0.0:
                temp8len = scale_expansion_zeroelim(cc, adxtail, temp8)
                temp16alen = scale_expansion_zeroelim(
                    temp8[:temp8len], bdytail, temp16a
                )
                finlength = fast_expansion_sum_zeroelim(
                    fin1[:finlength], temp16a[:temp16alen], fin2
                )
                fin2, fin1 = fin1, fin2

            if cdytail != 0.0:
                temp8len = scale_expansion_zeroelim(bb, -adxtail, temp8)
                temp16alen = scale_expansion_zeroelim(
                    temp8[:temp8len], cdytail, temp16a
                )
                finlength = fast_expansion_sum_zeroelim(
                    fin1[:finlength], temp16a[:temp16alen], fin2
                )
                fin2, fin1 = fin1, fin2

            temp32alen = scale_expansion_zeroelim(axtbct[:axtbctlen], adxtail, temp32a)
            axtbctt = [0.0] * 8
            axtbcttlen = scale_expansion_zeroelim(bctt[:bcttlen], adxtail, axtbctt)
            temp16alen = scale_expansion_zeroelim(
                axtbctt[:axtbcttlen], 2.0 * adx, temp16a
            )
            temp16blen = scale_expansion_zeroelim(
                axtbctt[:axtbcttlen], adxtail, temp16b
            )
            temp32blen = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp16b[:temp16blen], temp32b
            )
            temp64len = fast_expansion_sum_zeroelim(
                temp32a[:temp32alen], temp32b[:temp32blen], temp64
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp64[:temp64len], fin2
            )
            fin2, fin1 = fin1, fin2

        if adytail != 0.0:
            temp16alen = scale_expansion_zeroelim(aytbc[:aytbclen], adytail, temp16a)
            aytbct = [0.0] * 16
            aytbctlen = scale_expansion_zeroelim(bct[:bctlen], adytail, aytbct)
            temp32alen = scale_expansion_zeroelim(
                aytbct[:aytbctlen], 2.0 * ady, temp32a
            )
            temp48len = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp32a[:temp32alen], temp48
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp48[:temp48len], fin2
            )
            fin2, fin1 = fin1, fin2

            temp32alen = scale_expansion_zeroelim(aytbct[:aytbctlen], adytail, temp32a)
            aytbctt = [0.0] * 8
            aytbcttlen = scale_expansion_zeroelim(bctt[:bcttlen], adytail, aytbctt)
            temp16alen = scale_expansion_zeroelim(
                aytbctt[:aytbcttlen], 2.0 * ady, temp16a
            )
            temp16blen = scale_expansion_zeroelim(
                aytbctt[:aytbcttlen], adytail, temp16b
            )
            temp32blen = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp16b[:temp16blen], temp32b
            )
            temp64len = fast_expansion_sum_zeroelim(
                temp32a[:temp32alen], temp32b[:temp32blen], temp64
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp64[:temp64len], fin2
            )
            fin2, fin1 = fin1, fin2

    if bdxtail != 0.0 or bdytail != 0.0:
        catt = [0.0] * 4
        cat = [0.0] * 8

        if cdxtail != 0.0 or cdytail != 0.0 or adxtail != 0.0 or adytail != 0.0:
            (ti1, ti0) = two_product(cdxtail, ady)
            (tj1, tj0) = two_product(cdx, adytail)
            (u3, u2, u1, u0) = two_two_sum(ti1, ti0, tj1, tj0)
            u = [u0, u1, u2, u3]
            negate = -cdy
            (ti1, ti0) = two_product(adxtail, negate)
            negate = -cdytail
            (tj1, tj0) = two_product(adx, negate)
            (v3, v2, v1, v0) = two_two_sum(ti1, ti0, tj1, tj0)
            v = [v0, v1, v2, v3]
            catlen = fast_expansion_sum_zeroelim(u, v, cat)

            (ti1, ti0) = two_product(cdxtail, adytail)
            (tj1, tj0) = two_product(adxtail, cdytail)
            (catt3, catt2, catt1, catt0) = two_two_diff(ti1, ti0, tj1, tj0)
            catt = [catt0, catt1, catt2, catt3]
            cattlen = 4
        else:
            cat[0] = 0.0
            catlen = 1
            catt[0] = 0.0
            cattlen = 1

        if bdxtail != 0.0:
            temp16alen = scale_expansion_zeroelim(bxtca[:bxtcalen], bdxtail, temp16a)
            bxtcat = [0.0] * 16
            bxtcatlen = scale_expansion_zeroelim(cat[:catlen], bdxtail, bxtcat)
            temp32alen = scale_expansion_zeroelim(
                bxtcat[:bxtcatlen], 2.0 * bdx, temp32a
            )
            temp48len = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp32a[:temp32alen], temp48
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp48[:temp48len], fin2
            )
            fin2, fin1 = fin1, fin2

            if cdytail != 0.0:
                temp8len = scale_expansion_zeroelim(aa, bdxtail, temp8)
                temp16alen = scale_expansion_zeroelim(
                    temp8[:temp8len], cdytail, temp16a
                )
                finlength = fast_expansion_sum_zeroelim(
                    fin1[:finlength], temp16a[:temp16alen], fin2
                )
                fin2, fin1 = fin1, fin2

            if adytail != 0.0:
                temp8len = scale_expansion_zeroelim(cc, -bdxtail, temp8)
                temp16alen = scale_expansion_zeroelim(
                    temp8[:temp8len], adytail, temp16a
                )
                finlength = fast_expansion_sum_zeroelim(
                    fin1[:finlength], temp16a[:temp16alen], fin2
                )
                fin2, fin1 = fin1, fin2

            temp32alen = scale_expansion_zeroelim(bxtcat[:bxtcatlen], bdxtail, temp32a)
            bxtcatt = [0.0] * 8
            bxtcattlen = scale_expansion_zeroelim(catt[:cattlen], bdxtail, bxtcatt)
            temp16alen = scale_expansion_zeroelim(
                bxtcatt[:bxtcattlen], 2.0 * bdx, temp16a
            )
            temp16blen = scale_expansion_zeroelim(
                bxtcatt[:bxtcattlen], bdxtail, temp16b
            )
            temp32blen = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp16b[:temp16blen], temp32b
            )
            temp64len = fast_expansion_sum_zeroelim(
                temp32a[:temp32alen], temp32b[:temp32blen], temp64
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp64[:temp64len], fin2
            )
            fin2, fin1 = fin1, fin2

        if bdytail != 0.0:
            temp16alen = scale_expansion_zeroelim(bytca[:bytcalen], bdytail, temp16a)
            bytcat = [0.0] * 16
            bytcatlen = scale_expansion_zeroelim(cat[:catlen], bdytail, bytcat)
            temp32alen = scale_expansion_zeroelim(
                bytcat[:bytcatlen], 2.0 * bdy, temp32a
            )
            temp48len = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp32a[:temp32alen], temp48
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp48[:temp48len], fin2
            )
            fin2, fin1 = fin1, fin2

            temp32alen = scale_expansion_zeroelim(bytcat[:bytcatlen], bdytail, temp32a)
            bytcatt = [0.0] * 8
            bytcattlen = scale_expansion_zeroelim(catt[:cattlen], bdytail, bytcatt)
            temp16alen = scale_expansion_zeroelim(
                bytcatt[:bytcattlen], 2.0 * bdy, temp16a
            )
            temp16blen = scale_expansion_zeroelim(
                bytcatt[:bytcattlen], bdytail, temp16b
            )
            temp32blen = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp16b[:temp16blen], temp32b
            )
            temp64len = fast_expansion_sum_zeroelim(
                temp32a[:temp32alen], temp32b[:temp32blen], temp64
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp64[:temp64len], fin2
            )
            fin2, fin1 = fin1, fin2

    if cdxtail != 0.0 or cdytail != 0.0:
        abtt = [0.0] * 4
        abt = [0.0] * 8

        if adxtail != 0.0 or adytail != 0.0 or bdxtail != 0.0 or bdytail != 0.0:
            (ti1, ti0) = two_product(adxtail, bdy)
            (tj1, tj0) = two_product(adx, bdytail)
            (u3, u2, u1, u0) = two_two_sum(ti1, ti0, tj1, tj0)
            u = [u0, u1, u2, u3]
            negate = -ady
            (ti1, ti0) = two_product(bdxtail, negate)
            negate = -adytail
            (tj1, tj0) = two_product(bdx, negate)
            (v3, v2, v1, v0) = two_two_sum(ti1, ti0, tj1, tj0)
            v = [v0, v1, v2, v3]
            abtlen = fast_expansion_sum_zeroelim(u, v, abt)

            (ti1, ti0) = two_product(adxtail, bdytail)
            (tj1, tj0) = two_product(bdxtail, adytail)
            (abtt3, abtt2, abtt1, abtt0) = two_two_diff(ti1, ti0, tj1, tj0)
            abtt = [abtt0, abtt1, abtt2, abtt3]
            abttlen = 4
        else:
            abt[0] = 0.0
            abtlen = 1
            abtt[0] = 0.0
            abttlen = 1

        if cdxtail != 0.0:
            temp16alen = scale_expansion_zeroelim(cxtab[:cxtablen], cdxtail, temp16a)
            cxtabt = [0.0] * 16
            cxtabtlen = scale_expansion_zeroelim(abt[:abtlen], cdxtail, cxtabt)
            temp32alen = scale_expansion_zeroelim(
                cxtabt[:cxtabtlen], 2.0 * cdx, temp32a
            )
            temp48len = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp32a[:temp32alen], temp48
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp48[:temp48len], fin2
            )
            fin2, fin1 = fin1, fin2

            if adytail != 0.0:
                temp8len = scale_expansion_zeroelim(bb, cdxtail, temp8)
                temp16alen = scale_expansion_zeroelim(
                    temp8[:temp8len], adytail, temp16a
                )
                finlength = fast_expansion_sum_zeroelim(
                    fin1[:finlength], temp16a[:temp16alen], fin2
                )
                fin2, fin1 = fin1, fin2

            if bdytail != 0.0:
                temp8len = scale_expansion_zeroelim(aa, -cdxtail, temp8)
                temp16alen = scale_expansion_zeroelim(
                    temp8[:temp8len], bdytail, temp16a
                )
                finlength = fast_expansion_sum_zeroelim(
                    fin1[:finlength], temp16a[:temp16alen], fin2
                )
                fin2, fin1 = fin1, fin2

            temp32alen = scale_expansion_zeroelim(cxtabt[:cxtabtlen], cdxtail, temp32a)
            cxtabtt = [0.0] * 8
            cxtabttlen = scale_expansion_zeroelim(abtt[:abttlen], cdxtail, cxtabtt)
            temp16alen = scale_expansion_zeroelim(
                cxtabtt[:cxtabttlen], 2.0 * cdx, temp16a
            )
            temp16blen = scale_expansion_zeroelim(
                cxtabtt[:cxtabttlen], cdxtail, temp16b
            )
            temp32blen = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp16b[:temp16blen], temp32b
            )
            temp64len = fast_expansion_sum_zeroelim(
                temp32a[:temp32alen], temp32b[:temp32blen], temp64
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp64[:temp64len], fin2
            )
            fin2, fin1 = fin1, fin2
        #
        if cdytail != 0.0:
            temp16alen = scale_expansion_zeroelim(cytab[:cytablen], cdytail, temp16a)
            cytabt = [0.0] * 16
            cytabtlen = scale_expansion_zeroelim(abt[:abtlen], cdytail, cytabt)
            temp32alen = scale_expansion_zeroelim(
                cytabt[:cytabtlen], 2.0 * cdy, temp32a
            )
            temp48len = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp32a[:temp32alen], temp48
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp48[:temp48len], fin2
            )
            fin2, fin1 = fin1, fin2

            temp32alen = scale_expansion_zeroelim(cytabt[:cytabtlen], cdytail, temp32a)
            cytabtt = [0.0] * 8
            cytabttlen = scale_expansion_zeroelim(abtt[:abttlen], cdytail, cytabtt)
            temp16alen = scale_expansion_zeroelim(
                cytabtt[:cytabttlen], 2.0 * cdy, temp16a
            )
            temp16blen = scale_expansion_zeroelim(
                cytabtt[:cytabttlen], cdytail, temp16b
            )
            temp32blen = fast_expansion_sum_zeroelim(
                temp16a[:temp16alen], temp16b[:temp16blen], temp32b
            )
            temp64len = fast_expansion_sum_zeroelim(
                temp32a[:temp32alen], temp32b[:temp32blen], temp64
            )
            finlength = fast_expansion_sum_zeroelim(
                fin1[:finlength], temp64[:temp64len], fin2
            )
            fin2, fin1 = fin1, fin2

    return fin1[finlength - 1]


def scale_expansion_zeroelim(e, b, h):
    (bhi, blo) = split(b)
    (Q, hh) = two_product_presplit(e[0], b, bhi, blo)
    hindex = 0
    if hh != 0.0:
        h[hindex] = hh
        hindex += 1
    for eindex in range(1, len(e)):
        enow = e[eindex]
        (product1, product0) = two_product_presplit(enow, b, bhi, blo)
        (sum, hh) = two_sum(Q, product0)
        if hh != 0.0:
            h[hindex] = hh
            hindex += 1
        (new_q, hh) = fast_two_sum(product1, sum)
        Q = new_q
        if hh != 0.0:
            h[hindex] = hh
            hindex += 1
    if Q != 0.0 or hindex == 0:
        h[hindex] = Q
        hindex += 1
    return hindex


def two_product(a, b):
    x = a * b
    return (x, two_product_tail(a, b, x))


def two_product_tail(a, b, x):
    (ahi, alo) = split(a)
    (bhi, blo) = split(b)
    err1 = x - (ahi * bhi)
    err2 = err1 - (alo * bhi)
    err3 = err2 - (ahi * blo)
    return (alo * blo) - err3


def split(a):
    c = SPLITTER * a
    abig = c - a
    ahi = c - abig
    alo = a - ahi
    return (ahi, alo)


def two_product_presplit(a, b, bhi, blo):
    x = a * b
    (ahi, alo) = split(a)
    err1 = x - ahi * bhi
    err2 = err1 - alo * bhi
    err3 = err2 - ahi * blo
    y = alo * blo - err3
    return (x, y)


def two_two_diff(a1, a0, b1, b0):
    (j, _r0, x0) = two_one_diff(a1, a0, b0)
    (x3, x2, x1) = two_one_diff(j, _r0, b1)
    return (x3, x2, x1, x0)


def two_one_diff(a1, a0, b):
    (i, x0) = two_diff(a0, b)
    (x2, x1) = two_sum(a1, i)
    return (x2, x1, x0)


def two_diff(a, b):
    x = a - b
    return (x, two_diff_tail(a, b, x))


def two_diff_tail(a, b, x):
    bvirt = a - x
    avirt = x + bvirt
    bround = bvirt - b
    around = a - avirt
    return around + bround


def two_sum(a, b):
    x = a + b
    return (x, two_sum_tail(a, b, x))


def two_sum_tail(a, b, x):
    bvirt = x - a
    avirt = x - bvirt
    bround = b - bvirt
    around = a - avirt
    return around + bround


def estimate(e):
    q = e[0]
    for cur in e[1:]:
        q += cur
    return q


def fast_expansion_sum_zeroelim(e, f, h):
    enow = e[0]
    fnow = f[0]
    eindex = 0
    findex = 0
    if (fnow > enow) == (fnow > -enow):
        Q = enow
        eindex += 1
    else:
        Q = fnow
        findex += 1
    hindex = 0
    if eindex < len(e) and findex < len(f):
        enow = e[eindex]
        fnow = f[findex]
        if (fnow > enow) == (fnow > -enow):
            r = fast_two_sum(enow, Q)
            Qnew = r[0]
            hh = r[1]
            eindex += 1
        else:
            r = fast_two_sum(fnow, Q)
            Qnew = r[0]
            hh = r[1]
            findex += 1
        Q = Qnew
        if hh != 0.0:
            h[hindex] = hh
            hindex += 1
        while eindex < len(e) and findex < len(f):
            enow = e[eindex]
            fnow = f[findex]
            if (fnow > enow) == (fnow > -enow):
                r = two_sum(Q, enow)
                Qnew = r[0]
                hh = r[1]
                eindex += 1
            else:
                r = two_sum(Q, fnow)
                Qnew = r[0]
                hh = r[1]
                findex += 1
            Q = Qnew
            if hh != 0.0:
                h[hindex] = hh
                hindex += 1
    while eindex < len(e):
        enow = e[eindex]
        r = two_sum(Q, enow)
        Qnew = r[0]
        hh = r[1]
        Q = Qnew
        eindex += 1
        if hh != 0.0:
            h[hindex] = hh
            hindex += 1
    while findex < len(f):
        fnow = f[findex]
        r = two_sum(Q, fnow)
        Qnew = r[0]
        hh = r[1]
        Q = Qnew
        findex += 1
        if hh != 0.0:
            h[hindex] = hh
            hindex += 1
    if Q != 0.0 or hindex == 0:
        h[hindex] = Q
        hindex += 1
    return hindex


def fast_two_sum_tail(a, b, x):
    bvirt = x - a
    return b - bvirt


def fast_two_sum(a, b):
    x = a + b
    return (x, fast_two_sum_tail(a, b, x))


def square_tail(a, x):
    (ahi, alo) = split(a)
    err1 = x - ahi * ahi
    err3 = err1 - (ahi + ahi) * alo
    return alo * alo - err3


def square(a):
    x = a * a
    return (x, square_tail(a, x))


def two_one_sum(a1, a0, b):
    (_i, x0) = two_sum(a0, b)
    (x2, x1) = two_sum(a1, _i)
    return (x2, x1, x0)


def two_two_sum(a1, a0, b1, b0):
    (_j, _r0, x0) = two_one_sum(a1, a0, b0)
    (x3, x2, x1) = two_one_sum(_j, _r0, b1)
    return (x3, x2, x1, x0)


if __name__ == "__main__":
    assert (
        orient2d(
            (4.60756993660171e-11, 7.534734631999743e-11),
            (1.0000000000955178, 1.000000000071394),
            (2.000000000082655, 2.000000000005136),
        )
        < 0
    )
    assert incircle([0, -1], [1, 0], [0, 1], [-0.5, 0]) > 0
    assert incircle([0, -1], [1, 0], [0, 1], [-1, 0]) == 0
    assert incircle([0, -1], [1, 0], [0, 1], [-1.5, 0]) < 0
